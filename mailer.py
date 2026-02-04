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
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; }}
            .container {{ max-width: 800px; margin: 20px auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .news-item {{ margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #eee; }}
            .news-title {{ font-size: 18px; font-weight: bold; color: #2980b9; text-decoration: none; }}
            .news-source {{ font-size: 12px; color: #7f8c8d; margin-bottom: 5px; }}
            .news-summary {{ font-size: 14px; line-height: 1.6; color: #34495e; }}
            .footer {{ font-size: 12px; color: #bdc3c7; text-align: center; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>每日全球科技新闻速报 ({today})</h1>
            <p>为您精选 20 条国内外热门科技动态：</p>
    """
    
    for item in processed_news:
        html_content += f"""
        <div class="news-item">
            <div class="news-source">{item['source']}</div>
            <a class="news-title" href="{item['link']}">{item['title']}</a>
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
