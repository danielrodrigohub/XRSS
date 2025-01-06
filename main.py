import os
import sys
import datetime
import uvicorn

from typing import List
from logging import getLogger
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from datetime import timedelta, datetime
from twikit import Tweet as TwikitTweet, Client as TwikitClient
from fastapi import FastAPI, Response, Query
from feedgen.feed import FeedGenerator


load_dotenv()

# Check required environment variables
required_env_vars = {
    "TWITTER_USERNAME": "Twitter username for authentication",
    "TWITTER_EMAIL": "Twitter email for authentication",
    "TWITTER_PASSWORD": "Twitter password for authentication"
}

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


app = FastAPI()
logger = getLogger("xrss")
twikit_client = TwikitClient('en-US')

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


@app.post("/")
async def get_tweets(
    usernames: List[str],
    include_posts: bool = True,
    include_replies: bool = True,
    include_retweets: bool = True,
    include_quotes: bool = True,
):
    """
    Fetch and filter tweets from specified Twitter users.

    This endpoint authenticates with Twitter and retrieves tweets from the specified users,
    applying the requested filters. It handles various types of tweets including posts,
    replies, retweets, and quotes.

    Args:
        usernames (List[str]): List of Twitter usernames to fetch tweets from
        include_posts (bool, optional): Include regular posts. Defaults to True.
        include_replies (bool, optional): Include reply tweets. Defaults to True.
        include_retweets (bool, optional): Include retweets. Defaults to True.
        include_quotes (bool, optional): Include quote tweets. Defaults to True.

    Returns:
        dict: A dictionary where keys are usernames and values are lists of tweet objects.
              Each tweet object contains:
              - created_at: Tweet creation timestamp
              - type: Tweet type (Post/Reply/Retweet/Quote/Thread)
              - id: Tweet ID
              - full_text: Cleaned tweet text
              - in_reply_to: List of tweets this tweet is replying to (if any)

    Raises:
        Exception: If authentication with Twitter fails
    """

    try:
        twikit_client.load_cookies("cookies.json")
        await twikit_client.get_available_locations()
    except Exception as e:
        print(e)
        await twikit_client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        twikit_client.save_cookies("cookies.json")

    tweets = {}

    tweet_types = []

    if include_posts or include_retweets or include_quotes:
        tweet_types.append("Tweets")

    if include_replies:
        tweet_types.append("Replies")

    for username in usernames:

        user = await twikit_client.get_user_by_screen_name(username) # in guest mode, we can only get user by id

        for _tweet_type in tweet_types:

            user_tweets = list(await user.get_tweets(tweet_type=_tweet_type))
            user_tweets.sort(key=lambda x: datetime.strptime(x.created_at, "%a %b %d %H:%M:%S +0000 %Y"), reverse=True)

            # FIXME: here I can have tweets in double
            # Do not add if already in the dict
            tweets[username] = [{
                "created_at": tweet.created_at,
                "type": _get_tweet_type(tweet, user.id),
                "id": tweet.id,
                "full_text": clean_tweet(tweet.full_text),
                "in_reply_to": [{
                        "id": _reply.id,
                        "full_text": clean_tweet(_reply.full_text),
                        "username": _reply.user.screen_name,
                        "user_id": _reply.user.id,
                        "created_at": _reply.created_at,
                    } for _reply in tweet.replies
                ] if tweet.replies is not None else [], # [some tweet, answer from the target user]
                } for tweet in user_tweets
                if (include_posts and _get_tweet_type(tweet, user.id) == "Post")
                or (include_replies and _get_tweet_type(tweet, user.id) == "Reply")
                or (include_retweets and _get_tweet_type(tweet, user.id) == "Retweet")
                or (include_quotes and _get_tweet_type(tweet, user.id) == "Quote")
            ]

    # Remove duplicates
    for username, user_tweets in tweets.items():
        ids = set()
        tweets[username] = [tweet for tweet in user_tweets if tweet["id"] not in ids and not ids.add(tweet["id"])]

    return tweets


@app.get("/feed.xml")
async def get_feed(
    usernames: List[str] = Query(["ylecun", "AndrewYNg", "karpathy", "sama", "geoffreyhinton"]),
    include_posts: bool = True,
    include_replies: bool = True,
    include_retweets: bool = True,
    include_quotes: bool = True,
):
    """
    Generate an RSS feed from specified Twitter accounts.

    This endpoint creates an RSS feed containing the latest tweets from specified Twitter accounts.
    It supports filtering different types of tweets and presents them in a standard RSS format.

    Args:
        usernames (List[str], optional): List of Twitter usernames to include in the feed.
            Defaults to ["ylecun", "AndrewYNg", "karpathy", "sama", "geoffreyhinton"].
        include_posts (bool, optional): Include regular posts. Defaults to True.
        include_replies (bool, optional): Include reply tweets. Defaults to True.
        include_retweets (bool, optional): Include retweets. Defaults to True.
        include_quotes (bool, optional): Include quote tweets. Defaults to True.

    Returns:
        Response: An RSS feed in XML format containing the filtered tweets.
                 Each entry includes:
                 - Title: Tweet type and author
                 - Link: URL to the original tweet
                 - Description: Tweet content
                 - Publication date: Tweet creation time
                 - Author: Twitter username

    Note:
        The feed is formatted according to standard RSS specifications and can be
        consumed by any RSS reader.
    """

    fg = FeedGenerator()
    fg.title('The "Totally Not Twitter" Feed')
    fg.description('Your favorite bird site content, now in RSS form! (Please don\'t tell Elon)')
    fg.link(href='https://definitely-not-tracking-tweets.com')
    fg.language('en')

    tweets_data = await get_tweets(
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
            fe.pubDate(datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y").astimezone(ZoneInfo("UTC"))) # Datetime object has no timezone info
            fe.author({'name': username})
            fe.guid(f"https://twitter.com/{username}/status/{tweet['id']}", permalink=True)

    return Response(content=fg.rss_str(), media_type="application/rss+xml")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
