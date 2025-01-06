# 🌟 XRSS - Twitter to RSS, But Cooler

[![License](https://img.shields.io/github/license/thytu/XRSS)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

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
git clone https://github.com/thytu/xrss.git
cd xrss
```

2. Copy the example environment file and fill in your Twitter credentials:
```bash
cp .env.example .env
```

3. Choose your preferred installation method:

### Using Docker (recommended)
```bash
docker compose up -d
```

### Manual Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install .  # For basic installation
# OR
pip install ".[dev]"  # For development installation with testing tools

# Run the service
python main.py
```

The service will be available at:
- 📰 RSS Feed: `http://localhost:8000/feed.xml`
- 📚 API Docs: `http://localhost:8000/docs`

## 🔌 API Documentation

### 📡 GET /feed.xml
Get RSS feed for specified Twitter accounts.

#### Query Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| usernames | List[str] | ["ylecun", ...] | List of Twitter usernames |
| include_posts | bool | true | Include regular posts |
| include_replies | bool | true | Include replies |
| include_retweets | bool | true | Include retweets |
| include_quotes | bool | true | Include quote tweets |

#### Example
```
http://localhost:8000/feed.xml?usernames=ylecun&usernames=karpathy&include_replies=false
```

### 🔍 POST /
Raw API endpoint to fetch tweets.

#### Request Body
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

### Required Environment Variables
| Variable | Description |
|----------|-------------|
| TWITTER_USERNAME | Your Twitter username |
| TWITTER_EMAIL | Your Twitter email |
| TWITTER_PASSWORD | Your Twitter password |
| REDIS_URL | Redis connection URL |

### Optional Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| CACHE_TTL | 1800 | Cache duration in seconds |
| BACKGROUND_REFRESH_INTERVAL | 1500 | Background refresh interval in seconds |

## 🚄 Performance Optimizations

- 🗄️ Redis caching with configurable TTL
- 🔄 Background refresh before cache expiration
- 🚦 Rate limiting (2 concurrent requests, 1-second delay)
- ⚡ Parallel processing of requests
- 🔄 Efficient connection pooling
- 📦 Optimized data serialization

## 🧪 Testing

```bash
# Install with development dependencies if you haven't already
pip install ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest  # Coverage is included in default pytest configuration
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⭐ Show Your Support

If you find this project useful (and before Twitter's lawyers find it), please give it a star! It helps others discover the project and makes all the potential legal trouble worth it! 😄
