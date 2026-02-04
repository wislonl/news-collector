import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import SENDER_EMAIL, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT
from datetime import datetime

def send_email(processed_news, processed_repos=None):
    """
    发送美化的 HTML 邮件，包含新闻和 GitHub Agent 趋势
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
            .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; margin-bottom: 40px; border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; }}
            h1 {{ color: #0f172a; font-size: 28px; margin: 0 0 10px 0; letter-spacing: -0.5px; }}
            .section-title {{ font-size: 22px; font-weight: 800; color: #0f172a; margin: 40px 0 20px 0; padding-left: 12px; border-left: 4px solid #3b82f6; }}
            .subtitle {{ color: #64748b; font-size: 16px; }}
            .news-item {{ margin-bottom: 20px; padding: 20px; border-radius: 12px; background: #ffffff; border: 1px solid #e2e8f0; }}
            .news-meta {{ font-size: 12px; font-weight: 600; color: #3b82f6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
            .news-title {{ font-size: 18px; font-weight: 700; color: #1e293b; text-decoration: none; display: block; margin-bottom: 8px; }}
            .news-summary {{ font-size: 14px; line-height: 1.6; color: #475569; margin: 0; }}
            
            /* GitHub Styles */
            .repo-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; }}
            .repo-card {{ padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fdfdfe; }}
            .repo-name {{ font-weight: 700; color: #0969da; text-decoration: none; font-size: 15px; margin-bottom: 6px; display: block; }}
            .repo-tag {{ display: inline-block; font-size: 11px; padding: 1px 6px; border-radius: 4px; background: #f1f5f9; color: #475569; margin-right: 4px; margin-bottom: 4px; }}
            .repo-desc {{ font-size: 13px; color: #334155; margin: 8px 0; line-height: 1.4; }}
            .repo-stats {{ font-size: 12px; color: #64748b; display: flex; align-items: center; gap: 12px; }}
            .star-icon {{ color: #eac54f; font-weight: bold; }}
            
            .footer {{ font-size: 13px; color: #94a3b8; text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid #f1f5f9; }}
            .badge {{ display: inline-block; padding: 2px 8px; background: #eff6ff; color: #3b82f6; border-radius: 6px; font-size: 11px; }}
            @media (max-width: 600px) {{ .repo-grid {{ grid-template-columns: 1fr; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 科技速递 | Tech & Agent Digest</h1>
                <div class="subtitle">📅 {today} · 智选全球科技精要与 AI 趋势</div>
            </div>

            <div class="section-title">📰 今日深度精选</div>
    """
    
    for i, item in enumerate(processed_news):
        icon = "📰"
        title_upper = item['title'].upper()
        if any(kw in title_upper for kw in ["AI", "人工智能", "LLM", "MODEL", "GPT"]): icon = "🤖"
        elif any(kw in title_upper for kw in ["APPLE", "苹果", "IPHONE", "MAC"]): icon = "🍎"
        elif any(kw in title_upper for kw in ["CHIP", "芯片", "NVIDIA", "GPU", "英伟达"]): icon = "🔌"
        
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

    if processed_repos:
        # Top 50 Agents (展示前 10 个详细卡片，后 40 个列表)
        html_content += '<div class="section-title">🏆 GitHub Agent 总榜 Top 50 (精选)</div>'
        html_content += '<div class="repo-grid">'
        for repo in processed_repos['top'][:10]:
            html_content += f"""
            <div class="repo-card">
                <a class="repo-name" href="{repo['link']}">{repo['full_name']}</a>
                <div>
                    <span class="repo-tag" style="background: #dcfce7; color: #166534;">{repo['type']}</span>
                    <span class="repo-tag">{repo['specs']}</span>
                </div>
                <p class="repo-desc">{repo['description']}</p>
                <div class="repo-stats">
                    <span><span class="star-icon">★</span> {repo['stars']:,}</span>
                </div>
            </div>
            """
        html_content += '</div>'

        # Rising Agents (展示前 10 个详细卡片)
        html_content += '<div class="section-title">🔥 GitHub 近期爆发 Agent 榜</div>'
        html_content += '<div class="repo-grid">'
        for repo in processed_repos['rising'][:10]:
            html_content += f"""
            <div class="repo-card">
                <a class="repo-name" href="{repo['link']}">{repo['full_name']}</a>
                <div>
                    <span class="repo-tag" style="background: #fef9c3; color: #854d0e;">{repo['type']}</span>
                    <span class="repo-tag">{repo['specs']}</span>
                </div>
                <p class="repo-desc">{repo['description']}</p>
                <div class="repo-stats">
                    <span><span class="star-icon">★</span> {repo['stars']:,}</span>
                </div>
            </div>
            """
        html_content += '</div>'
        
    html_content += """
            <div class="footer">
                本邮件由 AI 自动化系统生成。每日早间准时送达。<br>
                包含 GitHub 热门项目 AI 智能解析。
            </div>
        </div>
    </body>
    </html>
    """

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"【科技早报】{today} 全球趋势与 Agent 报告"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

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
