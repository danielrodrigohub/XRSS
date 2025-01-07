# flake8: noqa
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from xrss.main import (
    app,
    clean_tweet,
    get_cached_tweets,
    get_cached_user,
    refresh_user_tweets_cache,
)

client = TestClient(app)


@pytest.fixture
def mock_redis():  # type: ignore
    with patch("xrss.main.redis") as mock:
        mock.get = AsyncMock()
        mock.setex = AsyncMock()
        yield mock


@pytest.fixture
def mock_twikit_client():  # type: ignore
    with patch("xrss.main.twikit_client") as mock:
        mock.get_user_by_screen_name = AsyncMock()
        yield mock


def test_clean_tweet() -> None:
    """Test the clean_tweet function with various inputs."""
    # Test regular tweet
    assert clean_tweet("Hello world!") == "Hello world!"

    # Test retweet
    assert clean_tweet("RT @user: Hello world!") == "Hello world!"

    # Test complex retweet
    assert clean_tweet("RT @user123: This is a: complex: tweet") == "This is a: complex: tweet"


@pytest.mark.asyncio
async def test_get_cached_user(mock_redis: AsyncMock) -> None:
    """Test get_cached_user function."""
    username = "testuser"
    user_data = {
        "profile_image_url": "http://example.com/image.jpg",
        "name": "Test User",
        "screen_name": "testuser",
    }

    # Test cache hit
    mock_redis.get.return_value = json.dumps(user_data)
    result = await get_cached_user(username)
    assert result == user_data
    mock_redis.get.assert_called_once_with("user:testuser")

    # Test cache miss
    mock_redis.get.return_value = None
    result = await get_cached_user(username)
    assert result is None


@pytest.mark.asyncio
async def test_get_cached_tweets(mock_redis: AsyncMock) -> None:
    """Test get_cached_tweets function."""
    username = "testuser"
    tweets_data = [
        {
            "created_at": "Wed Dec 31 23:59:59 +0000 2023",
            "type": "Post",
            "id": "123456",
            "full_text": "Test tweet",
            "in_reply_to": [],
        }
    ]

    # Test cache hit
    mock_redis.get.return_value = json.dumps(tweets_data)
    result = await get_cached_tweets(username)
    assert result == tweets_data
    mock_redis.get.assert_called_once_with("tweets:testuser")


@pytest.mark.skip(reason="This test is flaky and should be rewritten")
@pytest.mark.asyncio
async def test_refresh_user_tweets_cache(
    mock_redis: AsyncMock, mock_twikit_client: AsyncMock
) -> None:
    """Test refresh_user_tweets_cache function."""
    username = "testuser"

    # Mock user data
    mock_user = MagicMock()
    mock_user.profile_image_url = "http://example.com/image.jpg"
    mock_user.name = "Test User"
    mock_user.screen_name = "testuser"
    mock_user.get_tweets = AsyncMock()

    # Mock tweets
    mock_tweet = MagicMock()
    mock_tweet.id = "123456"
    mock_tweet.created_at = "Wed Dec 31 23:59:59 +0000 2023"
    mock_tweet.full_text = "Test tweet"
    mock_tweet.replies = []
    mock_tweet.thread = None
    mock_tweet.retweeted_tweet = None
    mock_tweet.in_reply_to = None
    mock_tweet.is_quote_status = False

    mock_user.get_tweets.return_value = [mock_tweet]
    mock_twikit_client.get_user_by_screen_name.return_value = mock_user

    await refresh_user_tweets_cache(username)

    # Verify Redis calls
    assert mock_redis.setex.call_count == 2  # 1 for user data, 1 for tweets
