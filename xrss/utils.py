"""Utility functions for XRSS."""

import json
import logging
import os
import sys
from typing import Optional

logger = logging.getLogger("xrss")


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        level: Optional logging level (defaults to INFO if not specified)

    Returns:
        Configured logger instance
    """

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    logger.setLevel(level or logging.INFO)
    return logger


def clean_tweet(tweet: str) -> str:
    """
    Clean and format tweet text by removing retweet prefixes.

    Args:
        tweet: The original tweet text to clean

    Returns:
        Cleaned tweet text with retweet prefixes removed if present

    Example:
        >>> clean_tweet("RT @user: This is the actual content")
        "This is the actual content"
        >>> clean_tweet("Regular tweet without RT")
        "Regular tweet without RT"
    """

    if tweet.startswith("RT @"):
        colon_index = tweet.find(":")
        if colon_index != -1:
            return tweet[colon_index + 2 :]
    return tweet


def clean_cookies(cookie_file: str = "cookies.json") -> None:
    """
    Clean up cookie file to prevent authentication issues.

    Args:
        cookie_file: Path to the cookie file
    """

    if not os.path.exists(cookie_file):
        logger.warning(f"Cookie file not found: {cookie_file}")
        return

    try:
        with open(cookie_file, "r") as f:
            cookies = json.load(f)

        # Keep only the most recent ct0 cookie if multiple exist
        ct0_cookies = [c for c in cookies if isinstance(c, dict) and c.get("name") == "ct0"]

        if len(ct0_cookies) > 1:
            logger.warning("Found multiple ct0 cookies, removing all but the most recent")
            os.remove(cookie_file)

    except Exception as e:
        logger.error(f"Error cleaning cookies: {str(e)}")

        if os.path.exists(cookie_file):
            os.remove(cookie_file)
