# 每日科技新闻自动化收集与发送

这是一个基于 Python 和 GitHub Actions 的自动化项目，每天自动从全球热门科技网站抓取新闻，利用 Gemini AI 进行摘要和翻译，最后通过邮件发送。

## 功能特点
- **全球视野**：涵盖 36Kr, IT之家, TechCrunch, The Verge 等国内外 Top 10 科技媒体。
- **AI 赋能**：使用 Gemini 1.5 Flash 对新闻进行精简摘要（100字以内），自动翻译英文新闻。
- **精美格式**：生成 HTML 邮件，阅读体验更佳。
- **全自动化**：基于 GitHub Actions，无需购买服务器，每日定时运行。

## 快速开始

### 1. 本地测试
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 配置环境变量：
   在根目录创建 `.env` 文件：
   ```env
   GEMINI_API_KEY=你的Gemini_API_Key
   SMTP_PASSWORD=你的邮箱授权码
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

### 2. GitHub Actions 自动化部署
1. 将代码推送到你的 GitHub 仓库。
2. 在 GitHub 仓库设置中，依次进入 **Settings -> Secrets and variables -> Actions**。
3. 添加以下两个 Repository secrets：
   - `GEMINI_API_KEY`: 填入你的 Gemini API Key。
   - `SMTP_PASSWORD`: 填入你的 163 邮箱授权码。
4. 默认配置为每天北京时间早上 8:00 发送。

## 配置项
你可以在 `config.py` 中自定义新闻源及抓取数量。
