import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 配置 Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def process_news(all_news):
    """
    处理新闻：中文摘要，英文翻译+摘要
    """
    processed_list = []
    
    for lang, news_items in all_news.items():
        for item in news_items:
            # --- 关键修复：显式定义 prompt ---
            if lang == "zh":
                prompt = f"请为以下科技新闻生成一个100字以内的中文精简摘要。只需要返回摘要文本，不要有其他描述：\n标题：{item['title']}\n内容：{item['summary']}"
            else:
                prompt = f"请将以下英文科技新闻翻译成中文，并生成一个100字以内的中文精简摘要。只需要返回翻译后的摘要文本，不要有其他描述：\n标题：{item['title']}\n内容：{item['summary']}"
            
            try:
                print(f"Summarizing: {item['title'][:30]}...")
                response = model.generate_content(prompt)
                if response and response.text:
                    item['ai_summary'] = response.text.strip()
                else:
                    item['ai_summary'] = "AI 未返回有效内容。"
            except Exception as e:
                print(f"Gemini API Error for {item['title']}: {e}")
                item['ai_summary'] = "摘要生成失败，请点击链接查看原文。"
            
            processed_list.append(item)
            
    return processed_list
