# 🌟 XRSS - Twitter to RSS, But Cooler

> **Disclaimer**: This project might be against Twitter's GCU, so I'm not responsible for what you do with it, but hey... feel free to leave a star anyway! What's the worst that could happen? (Besides getting sued by a billionaire? '-')

Transform tweets into an elegant RSS feed with custom filters, user tracking, and real-time updates. Perfect for keeping up with your favorite Twitter personalities without the endless scrolling.

## ✨ Features

- 🔄 Convert Twitter/X feeds to RSS format
- 👥 Support for multiple Twitter accounts
- 🎯 Filter by tweet types (posts, replies, retweets, quotes)
- ⚡ Redis-based caching for fast responses
- 🛡️ Rate limiting to prevent API throttling
- 🐳 Docker and Docker Compose support
- 🔄 Background refresh for always fresh data

## 📋 Prerequisites

- 🐳 Docker and Docker Compose
- 🔑 Twitter/X account credentials

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/xrss.git
cd xrss
```

2. Copy the example environment file and fill in your Twitter credentials:
```bash
cp .env.example .env
```

3. Start the services using Docker Compose:
```bash
docker compose up -d
```

The service will be available at:
- 📰 RSS Feed: `http://localhost:8000/feed.xml`
- 📚 API Docs: `http://localhost:8000/docs`

## 🔌 API Endpoints

### 📡 GET /feed.xml
Get RSS feed for specified Twitter accounts.

Query parameters:
- `usernames`: List of Twitter usernames (default: ["ylecun", "AndrewYNg", "karpathy", "sama", "geoffreyhinton"])
- `include_posts`: Include regular posts (default: true)
- `include_replies`: Include replies (default: true)
- `include_retweets`: Include retweets (default: true)
- `include_quotes`: Include quote tweets (default: true)

Example:
```
http://localhost:8000/feed.xml?usernames=ylecun&usernames=karpathy&include_replies=false
```

### 🔍 POST /
Raw API endpoint to fetch tweets.

Request body:
```json
{
  "usernames": ["user1", "user2"],
  "include_posts": true,
  "include_replies": true,
  "include_retweets": true,
  "include_quotes": true
}
```

## ⚙️ Configuration

Required environment variables:
- `TWITTER_USERNAME`: Your Twitter username
- `TWITTER_EMAIL`: Your Twitter email
- `TWITTER_PASSWORD`: Your Twitter password
- `REDIS_URL`: Redis connection URL (default: redis://redis:6379)

Optional environment variables:
- `CACHE_TTL`: Cache duration in seconds (default: 1800 - 30 minutes)
- `BACKGROUND_REFRESH_INTERVAL`: Background refresh interval in seconds (default: 1500 - 25 minutes)

## 🚄 Performance Optimizations

- 🗄️ Redis caching with configurable TTL (default: 30 minutes)
- 🔄 Background refresh 5 minutes before cache expiration
- 🚦 Rate limiting (2 concurrent requests, 1-second delay)
- ⚡ Parallel processing of requests within rate limits

## 💻 Development

To run in development mode:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

## ⭐ Show Your Support

If you find this project useful (and before Twitter's lawyers find it), please give it a star! It helps others discover the project and makes all the potential legal trouble worth it! 😄
