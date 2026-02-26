import os

# 新闻源配置
NEWS_SOURCES = {
    "zh": [
        "https://36kr.com/feed",
        "https://www.ithome.com/rss/",
        "https://sspai.com/feed",
        "https://feeds.feedburner.com/solidot",
        "https://www.huxiu.com/rss/0.xml"
    ],
    "en": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.wired.com/feed/rss",
        "https://arstechnica.com/feed/",
        "https://www.engadget.com/rss.xml"
    ]
}

# 每天每个源抓取的热门新闻条数
NEWS_PER_SOURCE = 10

# 邮件配置 (优先使用环境变量)
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "jw.lee@163.com")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "jw.lee@163.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.163.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

# API 配置 (优先使用环境变量，GitHub Actions 会通过 secrets 注入)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
