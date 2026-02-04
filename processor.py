import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 配置 Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# 使用更稳定的 Gemini 1.5 Flash 模型
model = genai.GenerativeModel('gemini-1.5-flash')

def select_top_news(all_news, count=20):
    """
    让 AI 从一大堆新闻中筛选出最值得阅读的 20 条
    """
    # 提取所有标题
    titles = []
    flat_news = []
    for lang, items in all_news.items():
        for i, item in enumerate(items):
            tag = f"{lang}_{i}"
            titles.append(f"[{tag}] {item['title']}")
            item['temp_tag'] = tag
            flat_news.append(item)
    
    if not flat_news:
        return []

    # 构建 Prompt
    prompt = f"""以下是今天的科技新闻标题列表。请从中挑选出最重要、最受关注、或者对科技行业有重大影响的 {count} 条新闻。
只需返回选中新闻的索引标签（例如 [zh_0], [en_5]），用英文逗号分隔，不要有任何其他解释文字。

新闻列表：
"""
    prompt += "\n".join(titles)
    
    try:
        print(f"AI is selecting top {count} news from {len(flat_news)} items...")
        # 增加安全设置防止筛选阶段被拦截
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }
        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        if not response or not response.text:
            print("AI failed to select news, falling back to original list.")
            return flat_news[:count]
            
        # 解析返回的标签
        import re
        selected_tags = re.findall(r'\[(zh_\d+|en_\d+)\]', response.text)
        
        # 匹配回原始新闻对象
        selected_news = []
        news_map = {item['temp_tag']: item for item in flat_news}
        
        for tag in selected_tags:
            if tag in news_map:
                selected_news.append(news_map[tag])
        
        # 如果 AI 没选够或者选错，补齐
        if not selected_news:
            return flat_news[:count]
            
        return selected_news[:count]

    except Exception as e:
        print(f"Error during AI selection: {e}")
        return flat_news[:count]

def process_news(news_list):
    """
    处理新闻列表：生成摘要（如果是英文则翻译+摘要）
    """
    processed_list = []
    import time
    
    # 使用字典格式的安全设置
    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }
    
    for i, item in enumerate(news_list):
        is_english = item.get('lang') == 'en'
        
        if not is_english:
            prompt = f"请为以下科技新闻生成一个100字以内的中文精简摘要。只需要返回摘要文本内容，不要包含“摘要：”或“标题：”等字样：\n标题：{item['title']}\n内容：{item['summary']}"
        else:
            prompt = f"请将以下英文科技新闻翻译成中文，并生成一个100字以内的中文精简摘要。只需要返回摘要文本内容，不要包含“摘要：”或“翻译：”等字样：\n标题：{item['title']}\n内容：{item['summary']}"
        
        # 增加重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"[{i+1}/{len(news_list)}] Summarizing: {item['title'][:30]}...")
                response = model.generate_content(prompt, safety_settings=safety_settings)
                
                if response.candidates and response.candidates[0].content.parts:
                    item['ai_summary'] = response.text.strip()
                    break # 成功则跳出重试循环
                else:
                    raise Exception("Empty response or blocked")
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {item['title'][:20]}: {e}")
                if attempt == max_retries - 1:
                    item['ai_summary'] = "摘要生成失败，可能是内容触发了安全策略或 API 额度超限。请点击链接查看原文。"
                else:
                    time.sleep(2) # 失败后等待 2 秒重试
        
        processed_list.append(item)
        # 每次请求后稍微停顿，避免触发免费额度的频率限制 (RPM)
        time.sleep(1)
            
    return processed_list
