# 每日科技与 AI Agent 趋势自动化报告

这是一个基于 Python 和 GitHub Actions 的自动化项目，每天自动从全球热门科技网站及 GitHub 抓取最新动态，利用 Gemini AI 进行深度摘要和解析，最后通过精美的 HTML 邮件发送。

## 功能特点
- **全球视野**：涵盖 36Kr, IT之家, TechCrunch, The Verge 等国内外 Top 10 科技媒体。
- **GitHub Agent 追踪**：
    - **历史总榜**：自动追踪 GitHub 上 Stars 最高的 Top 50 AI Agent/Model 项目。
    - **黑马新秀**：实时抓取过去 30 天内快速上升的 Top 50 潜力项目。
- **AI 深度解析**：
    - 使用 Gemini 1.5 Flash 对新闻进行精简摘要及自动翻译。
    - **规格推断**：自动解析 GitHub 项目的类型（模型/框架/工具）、参数量（如 7B/70B）及核心功能。
- **精美可视化**：生成卡片式 HTML 邮件，包含智能内容图标、Star 徽章及响应式布局。
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
   GITHUB_TOKEN=你的GitHub_Token(可选,增加API配额)
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

### 2. GitHub Actions 自动化部署
1. 将代码推送到你的 GitHub 仓库。
2. 在 GitHub 仓库设置中，依次进入 **Settings -> Secrets and variables -> Actions**。
3. 添加以下 Repository secrets：
   - `GEMINI_API_KEY`: 填入你的 Gemini API Key。
   - `SMTP_PASSWORD`: 填入你的邮箱授权码。
   - `GITHUB_TOKEN`: (可选) 填入你的 GitHub Personal Access Token。
4. 默认配置为每天北京时间早上 8:00 发送。

## 配置项
你可以在 `config.py` 中自定义新闻源及抓取数量。
