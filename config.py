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
NEWS_PER_SOURCE = 2

# 邮件配置
SENDER_EMAIL = "jw.lee@163.com"
RECEIVER_EMAIL = "jw.lee@163.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
