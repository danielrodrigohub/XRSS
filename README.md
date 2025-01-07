# 🌟 XRSS - Your Twitter Feed, RSS-ified and Supercharged!

<div align="center">

[![License](https://img.shields.io/github/license/thytu/XRSS)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Docker Hub](https://img.shields.io/docker/pulls/thytu/xrss)](https://hub.docker.com/r/thytu/xrss)

<img src="https://i.ibb.co/87RF1jG/xrss.png" alt="XRSS Logo" width="200"/>

*Transform your Twitter experience into a delightful, distraction-free RSS feed!* 🚀

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

> **Note**: This project is a labor of love that transforms tweets into RSS feeds. While it might raise an eyebrow at Twitter HQ, we're all about making content more accessible! 🎭

## 🌈 What's XRSS?

XRSS is your passport to a cleaner, more organized Twitter experience. It transforms the chaotic Twitter timeline into a structured, filterable RSS feed that puts YOU in control. Perfect for researchers, developers, and anyone who loves their content well-organized!

### Why Choose XRSS?

- 🎯 **Laser-Focused**: Get exactly the content you want, nothing more
- 🚀 **Blazing Fast**: Redis-powered caching keeps everything snappy
- 🛠️ **Highly Customizable**: Filter by post types, users, and more
- 🐳 **Deploy Anywhere**: Docker-ready for instant deployment
- 🤝 **Developer Friendly**: Clean API with comprehensive documentation

## ✨ Features

Transform your Twitter experience with:

- 🎭 **Smart Feed Conversion**: Seamlessly transform Twitter/X feeds into clean RSS format
- 🎯 **Precision Filtering**: Cherry-pick exactly what you want to see (posts, replies, retweets, quotes)
- ⚡ **Lightning Fast**: Redis-powered caching system for instant responses
- 🛡️ **API Friendly**: Built-in rate limiting to keep you within bounds
- 🐳 **Deploy & Forget**: One-click deployment with Docker
- 🤖 **Always Fresh**: Background refresh keeps your content up-to-date

## 🚀 Getting Started

### Prerequisites

You'll need:
- 🐳 Docker & Docker Compose installed
- 🔑 Twitter/X account credentials
- ☕ A few minutes of your time

### Quick Setup

1. **Clone & Configure**
   ```bash
   # Get the example config
   curl -O https://raw.githubusercontent.com/thytu/xrss/main/.env.example
   mv .env.example .env
   # Edit .env with your Twitter credentials
   ```

2. **Choose Your Path**

   #### 🐳 Docker Way (Recommended)
   ```bash
   # Using Docker Compose (recommended)
   curl -O https://raw.githubusercontent.com/thytu/xrss/main/docker-compose.yml
   docker compose up -d

   # Or using Docker directly
   docker run -d \
     --name xrss \
     -p 8000:8000 \
     --env-file .env \
     vdematos/xrss:latest
   ```

   #### 🛠️ Manual Setup
   ```bash
   # Create your virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate

   # Install what you need
   pip install .            # Basic setup
   # OR
   pip install ".[dev]"    # Developer setup with testing goodies

   # Launch!
   python main.py
   ```

### 🎯 Access Your Feeds

Once running, your feeds are available at:
- 📰 RSS Feed: `http://localhost:8000/feed.xml`
- 📚 API Documentation: `http://localhost:8000/docs`

## 🔌 API Documentation

### Endpoints

#### 📡 GET `/feed.xml`
Your gateway to RSS-formatted Twitter feeds.

```http
GET /feed.xml?usernames=ylecun&usernames=karpathy&include_replies=false
```

| Parameter | Type | Default | Description |
|:----------|:-----|:---------|:------------|
| `usernames` | `List[str]` | `["ylecun"]` | Twitter handles to follow |
| `include_posts` | `bool` | `true` | Include regular tweets |
| `include_replies` | `bool` | `true` | Include reply tweets |
| `include_retweets` | `bool` | `true` | Include retweets |
| `include_quotes` | `bool` | `true` | Include quote tweets |

#### 🔍 POST `/`
Raw API endpoint for advanced users.

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

### 🔐 Required Environment Variables

| Variable | Description |
|:---------|:------------|
| `TWITTER_USERNAME` | Your Twitter handle |
| `TWITTER_EMAIL` | Your Twitter email |
| `TWITTER_PASSWORD` | Your Twitter password |
| `REDIS_URL` | Redis connection string |

### 🎛️ Optional Tweaks

| Variable | Default | What it Does |
|:---------|:--------|:-------------|
| `CACHE_TTL` | `1800` | How long to cache (seconds) |
| `BACKGROUND_REFRESH_INTERVAL` | `1500` | How often to refresh (seconds) |

## 🚄 Performance

We've optimized XRSS to be blazing fast:

- 🗄️ **Smart Caching**: Redis-powered with configurable TTL
- 🔄 **Proactive Updates**: Background refresh before cache expires
- 🚦 **Traffic Control**: Rate limiting (2 concurrent, 1s delay)
- ⚡ **Parallel Power**: Concurrent request processing
- 🔌 **Connection Smarts**: Efficient connection pooling
- 📦 **Data Efficiency**: Optimized serialization

## 🧪 Testing

```bash
# Get the dev goodies
pip install ".[dev]"

# Run the test suite
pytest

# Check the coverage
pytest  # Coverage included by default
```

## 🤝 Contributing

We love contributions! Here's how you can help:

1. 🍴 Fork it
2. 🌿 Create your branch: `git checkout -b feature/amazing-feature`
3. 🔄 Commit changes: `git commit -m 'Add amazing feature'`
4. ⤴️ Push to the branch: `git push origin feature/amazing-feature`
5. 🎯 Open a Pull Request

Check our [Contributing Guidelines](CONTRIBUTING.md) for more details!

## ⭐ Show Some Love

If this project helps you tame your Twitter feed, consider giving it a star! It helps others discover the project and makes our day! 🌟

---
<div align="center">

</div>
