# 🌟 XRSS - Twitter to RSS, But Cooler

> **Disclaimer**: This project might be against Twitter's GCU, so I'm not responsible for what you do with it, but hey... feel free to leave a star anyway! What's the worst that could happen? (Besides getting sued by a billionaire? '-')

Transform tweets into an elegant RSS feed with custom filters, user tracking, and real-time updates. Perfect for keeping up with your favorite Twitter personalities without the endless scrolling.

## ✨ Features

- 🔄 Convert Twitter timelines into RSS feeds
- 👥 Track multiple Twitter users simultaneously
- 🎯 Custom filtering options (posts, replies, retweets, quotes)
- ⚡ Real-time updates
- 🐳 Docker support for easy deployment

## 🚀 Quick Start

### Using Docker

```bash
# Clone the repository
git clone https://github.com/Thytu/XRSS.git
cd XRSS

# Create your .env file
cp .env.example .env
# Edit .env with your Twitter credentials

# Build and run with Docker
docker build -t xrss .
docker run -p 8000:8000 xrss
```

### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/Thytu/xrss.git
cd xrss
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
```bash
cp .env.example .env
# Edit .env with your credentials:
# TWITTER_USERNAME="your_username"
# TWITTER_EMAIL="your_email"
# TWITTER_PASSWORD="your_password"
```

4. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔧 Usage

Access your RSS feed at:
```
http://localhost:8000/feed.xml
```

### Query Parameters

- `usernames`: List of Twitter usernames to follow (comma-separated)
- `include_posts`: Include regular posts (default: true)
- `include_replies`: Include replies (default: true)
- `include_retweets`: Include retweets (default: true)
- `include_quotes`: Include quote tweets (default: true)

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Show Your Support

If you find this project useful (and before Twitter's lawyers find it), please give it a star! It helps others discover the project and makes all the potential legal trouble worth it! 😄
