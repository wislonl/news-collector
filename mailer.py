import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import SENDER_EMAIL, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT
from datetime import datetime

def send_email(processed_news):
    """
    发送美化的 HTML 邮件
    """
    password = os.getenv("SMTP_PASSWORD")
    if not password:
        print("Error: SMTP_PASSWORD not found.")
        return

    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构造 HTML 内容
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; }}
            h1 {{ color: #0f172a; font-size: 28px; margin: 0 0 10px 0; letter-spacing: -0.5px; }}
            .subtitle {{ color: #64748b; font-size: 16px; }}
            .news-item {{ margin-bottom: 30px; padding: 24px; border-radius: 12px; background: #ffffff; border: 1px solid #e2e8f0; transition: all 0.2s ease; }}
            .news-item:hover {{ border-color: #3b82f6; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1); }}
            .news-meta {{ font-size: 12px; font-weight: 600; color: #3b82f6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
            .news-title {{ font-size: 20px; font-weight: 700; color: #1e293b; text-decoration: none; display: block; margin-bottom: 12px; line-height: 1.4; }}
            .news-summary {{ font-size: 15px; line-height: 1.6; color: #475569; margin: 0; }}
            .footer {{ font-size: 13px; color: #94a3b8; text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid #f1f5f9; }}
            .badge {{ display: inline-block; padding: 2px 8px; background: #eff6ff; color: #3b82f6; border-radius: 6px; font-size: 11px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 科技速递 | Tech Digest</h1>
                <div class="subtitle">📅 {today} · 智选全球科技精要</div>
            </div>
    """
    
    for i, item in enumerate(processed_news):
        # 简单根据内容选择图标
        icon = "📰"
        title_upper = item['title'].upper()
        if any(kw in title_upper for kw in ["AI", "人工智能", "LLM", "MODEL", "GPT"]): icon = "🤖"
        elif any(kw in title_upper for kw in ["APPLE", "苹果", "IPHONE", "MAC"]): icon = "🍎"
        elif any(kw in title_upper for kw in ["TESLA", "特斯拉", "EV", "AUTO", "车"]): icon = "🚗"
        elif any(kw in title_upper for kw in ["CHIP", "芯片", "NVIDIA", "GPU", "英伟达"]): icon = "🔌"
        elif any(kw in title_upper for kw in ["SPACE", "SPACE X", "航天", "火箭"]): icon = "🌌"
        elif any(kw in title_upper for kw in ["CRYPTO", "BITCOIN", "WEB3", "BLOCKCHAIN"]): icon = "⛓️"
        
        html_content += f"""
        <div class="news-item">
            <div class="news-meta">
                <span class="badge">#{i+1}</span>
                <span>🌐 {item['source']}</span>
            </div>
            <a class="news-title" href="{item['link']}">{icon} {item['title']}</a>
            <p class="news-summary">{item['ai_summary']}</p>
        </div>
        """
        
    html_content += """
            <div class="footer">
                本邮件由 AI 自动化系统生成。每日早间准时送达。
            </div>
        </div>
    </body>
    </html>
    """

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"【科技早报】{today} 全球热门新闻整理"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # 使用 SSL 连接
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e # 抛出异常，让 GitHub Actions 显示失败，方便排查
