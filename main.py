import os
import sys
import json
import asyncio
import uvicorn

from typing import List, Dict, Any
from logging import getLogger
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from datetime import datetime
from twikit import Tweet as TwikitTweet, Client as TwikitClient
from fastapi import FastAPI, Response, Query, BackgroundTasks
from feedgen.feed import FeedGenerator
from redis import asyncio as aioredis


load_dotenv()

# Check required environment variables
required_env_vars = {
    "TWITTER_USERNAME": "Twitter username for authentication",
    "TWITTER_EMAIL": "Twitter email for authentication",
    "TWITTER_PASSWORD": "Twitter password for authentication",
    "REDIS_URL": "Redis connection URL (e.g., redis://localhost)"
}

# Optional environment variables with defaults
CACHE_TTL = int(os.getenv("CACHE_TTL", 1800))  # 30 minutes by default
BACKGROUND_REFRESH_INTERVAL = int(os.getenv("BACKGROUND_REFRESH_INTERVAL", 1500))  # 25 minutes by default

missing_vars = [var for var, desc in required_env_vars.items() if not os.getenv(var)]
if missing_vars:
    print("Error: Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}: {required_env_vars[var]}")
    print("\nPlease add them to your .env file")
    sys.exit(1)


USERNAME = os.environ["TWITTER_USERNAME"]
EMAIL = os.environ["TWITTER_EMAIL"]
PASSWORD = os.environ["TWITTER_PASSWORD"]
REDIS_URL = os.environ["REDIS_URL"]

# Rate limiting configuration
MAX_CONCURRENT_REQUESTS = 2  # Maximum number of concurrent requests to Twitter API
REQUEST_DELAY = 1.0  # Delay between requests in seconds
api_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

app = FastAPI()
logger = getLogger("xrss")
twikit_client = TwikitClient('en-US')
redis = aioredis.from_url(REDIS_URL, decode_responses=True)

def _get_tweet_type(tweet: TwikitTweet) -> str:
    """
    Determine the type of a tweet based on its characteristics.

    This function analyzes a tweet's properties to categorize it into one of the following types:
    - Thread: Part of a connected series of tweets
    - Retweet: A reshared tweet from another user
    - Reply: A response to another tweet
    - Quote: A tweet that quotes another tweet
    - Post: A standard, standalone tweet

    Args:
        tweet (TwikitTweet): The tweet object to analyze

    Returns:
        str: The categorized type of the tweet ("Thread", "Retweet", "Reply", "Quote", or "Post")

    Note:
        The reply detection is currently not working as expected (see FIXME comment in implementation)
    """

    if tweet.thread is not None:
        return "Thread"

    if tweet.retweeted_tweet is not None:
        return "Retweet"

    if (tweet.replies is not None and len(tweet.replies) > 0) or tweet.in_reply_to is not None:
        return "Reply"

    if tweet.is_quote_status is True:
        return "Quote"

    return "Post"


def clean_tweet(tweet: str) -> str:
    """
    Clean and format the tweet text by removing retweet prefixes.

    This function processes tweet text to improve readability by:
    1. Detecting if the tweet starts with "RT @"
    2. If found, removing the retweet prefix and any text up to the first colon
    3. Preserving the actual content that follows

    Args:
        tweet (str): The original tweet text to clean

    Returns:
        str: The cleaned tweet text with retweet prefixes removed if present,
             or the original text if no cleaning was needed

    Example:
        >>> clean_tweet("RT @user: This is the actual content")
        "This is the actual content"
        >>> clean_tweet("Regular tweet without RT")
        "Regular tweet without RT"
    """
    # Check if the tweet starts with "RT @" and remove the prefix
    if tweet.startswith("RT @"):
        # Find the index of the first colon (":")
        colon_index = tweet.find(":")
        # Extract the text after the colon
        if colon_index != -1:
            return tweet[colon_index + 2:]  # Skip the colon and the following space

    return tweet  # Return the original tweet if no match


async def rate_limited_request(coroutine):
    """Execute a coroutine with rate limiting."""
    async with api_semaphore:
        result = await coroutine
        await asyncio.sleep(REQUEST_DELAY)
        return result

async def refresh_user_tweets_cache(username: str) -> None:
    """Background task to refresh the cache for a user's tweets."""
    try:
        user = await rate_limited_request(twikit_client.get_user_by_screen_name(username))

        # Fetch tweets with rate limiting
        tasks = [
            rate_limited_request(user.get_tweets(tweet_type="Tweets")),
            rate_limited_request(user.get_tweets(tweet_type="Replies"))
        ]
        results = await asyncio.gather(*tasks)

        # Combine and process tweets
        all_tweets = []
        seen_tweet_ids = set()
        for tweet_list in results:
            for tweet in tweet_list:
                if tweet.id not in seen_tweet_ids:
                    all_tweets.append(tweet)
                    seen_tweet_ids.add(tweet.id)

        # Sort and process tweets
        all_tweets.sort(key=lambda x: datetime.strptime(x.created_at, "%a %b %d %H:%M:%S +0000 %Y"), reverse=True)

        processed_tweets = [{
            "created_at": tweet.created_at,
            "type": _get_tweet_type(tweet),
            "id": tweet.id,
            "full_text": clean_tweet(tweet.full_text),
            "in_reply_to": [{
                "id": _reply.id,
                "full_text": clean_tweet(_reply.full_text),
                "username": _reply.user.screen_name,
                "user_id": _reply.user.id,
                "created_at": _reply.created_at,
            } for _reply in (tweet.replies or [])]
        } for tweet in all_tweets]

        # Store in Redis with TTL
        await redis.setex(
            f"tweets:{username}",
            CACHE_TTL,
            json.dumps(processed_tweets)
        )

    except Exception as e:
        logger.error(f"Error refreshing cache for {username}: {str(e)}")

async def get_cached_tweets(username: str) -> List[Dict[str, Any]]:
    """Get tweets from cache or fetch if not available."""
    cache_key = f"tweets:{username}"
    cached_data = await redis.get(cache_key)

    if cached_data:
        return json.loads(cached_data)

    # If not in cache, fetch and cache
    await refresh_user_tweets_cache(username)
    cached_data = await redis.get(cache_key)
    return json.loads(cached_data) if cached_data else []

@app.post("/")
async def get_tweets(
    background_tasks: BackgroundTasks,
    usernames: List[str],
    include_posts: bool = True,
    include_replies: bool = True,
    include_retweets: bool = True,
    include_quotes: bool = True,
):
    """Optimized tweet fetching with caching and background refresh."""
    try:
        # Ensure authenticated
        if not os.path.exists("cookies.json"):
            await twikit_client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
            twikit_client.save_cookies("cookies.json")
        else:
            try:
                twikit_client.load_cookies("cookies.json")
                await twikit_client.get_available_locations()
            except Exception:
                await twikit_client.login(
                    auth_info_1=USERNAME,
                    auth_info_2=EMAIL,
                    password=PASSWORD
                )
                twikit_client.save_cookies("cookies.json")

        # Fetch tweets for all users with rate limiting
        tasks = [get_cached_tweets(username) for username in usernames]
        all_tweets = await asyncio.gather(*tasks)

        # Schedule background refresh for each user
        for username in usernames:
            background_tasks.add_task(refresh_user_tweets_cache, username)

        # Process and filter tweets
        result = {}
        for username, user_tweets in zip(usernames, all_tweets):
            result[username] = [
                tweet for tweet in user_tweets
                if (include_posts and tweet["type"] == "Post")
                or (include_replies and tweet["type"] == "Reply")
                or (include_retweets and tweet["type"] == "Retweet")
                or (include_quotes and tweet["type"] == "Quote")
            ]

        return result

    except Exception as e:
        logger.error(f"Error in get_tweets: {str(e)}")
        raise

@app.get("/feed.xml")
async def get_feed(
    background_tasks: BackgroundTasks,
    usernames: List[str] = Query(["ylecun", "AndrewYNg", "karpathy", "sama", "geoffreyhinton"]),
    include_posts: bool = True,
    include_replies: bool = True,
    include_retweets: bool = True,
    include_quotes: bool = True,
):
    """Optimized RSS feed generation with caching."""
    fg = FeedGenerator()
    fg.title('The "Totally Not Twitter" Feed')
    fg.description('Your favorite bird site content, now in RSS form! (Please don\'t tell Elon)')
    fg.link(href='https://definitely-not-tracking-tweets.com')
    fg.language('en')

    tweets_data = await get_tweets(
        background_tasks=background_tasks,
        usernames=usernames,
        include_posts=include_posts,
        include_replies=include_replies,
        include_retweets=include_retweets,
        include_quotes=include_quotes,
    )

    for username, tweets in tweets_data.items():
        for tweet in tweets:
            fe = fg.add_entry()
            fe.title(f"{tweet['type']} by {username}")
            fe.link(href=f"https://twitter.com/{username}/status/{tweet['id']}")
            fe.description(tweet['full_text'])
            fe.pubDate(datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y").astimezone(ZoneInfo("UTC")))
            fe.author({'name': username})
            fe.guid(f"https://twitter.com/{username}/status/{tweet['id']}", permalink=True)

    return Response(content=fg.rss_str(), media_type="application/rss+xml")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
