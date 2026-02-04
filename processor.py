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
    
    # 合并任务以减少 API 调用次数（或者逐条处理以保证稳定性）
    # 这里采用逐条处理，方便错误控制
    
    for lang, news_items in all_news.items():
        for item in news_items:
            # ... 保持 prompt 逻辑不变 ...
            try:
                # 显式使用 generate_content 之前先打印一下
                print(f"Summarizing: {item['title'][:30]}...")
                response = model.generate_content(prompt)
                # 检查 response 是否有有效文本
                if response and response.text:
                    item['ai_summary'] = response.text.strip()
                else:
                    item['ai_summary'] = "AI 未返回有效内容。"
            except Exception as e:
                print(f"Gemini API Error for {item['title']}: {e}")
                item['ai_summary'] = f"AI 摘要失败: {str(e)}"
            
            processed_list.append(item)
            
    return processed_list
