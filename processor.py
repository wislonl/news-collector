import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 配置 Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# 使用最新建议的模型名称
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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
        response = model.generate_content(prompt)
        
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
    
    # 设置安全设置以减少拦截
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    for item in news_list:
        lang = "en" if any(ord(c) < 128 for c in item['title'][:5]) and not any('\u4e00' <= c <= '\u9fff' for c in item['title']) else "zh"
        # 简单的语言判断，或者在抓取时就标记好
        # 这里为了兼容性，我们可以让 fetcher 传递 lang 属性，或者根据源判断
        
        is_english = item.get('lang') == 'en'
        
        if not is_english:
            prompt = f"请为以下科技新闻生成一个100字以内的中文精简摘要。只需要返回摘要文本，不要有其他描述：\n标题：{item['title']}\n内容：{item['summary']}"
        else:
            prompt = f"请将以下英文科技新闻翻译成中文，并生成一个100字以内的中文精简摘要。只需要返回翻译后的摘要文本，不要有其他描述：\n标题：{item['title']}\n内容：{item['summary']}"
        
        try:
            print(f"Summarizing: {item['title'][:30]}...")
            # 增加安全设置调用
            response = model.generate_content(prompt, safety_settings=safety_settings)
            
            # 安全检查 response.text 可能会抛出错误（如果被 block）
            if response.candidates and response.candidates[0].content.parts:
                item['ai_summary'] = response.text.strip()
            else:
                # 尝试获取反馈信息
                feedback = getattr(response, 'prompt_feedback', 'No feedback available')
                print(f"Blocked or Empty response for {item['title']}. Feedback: {feedback}")
                item['ai_summary'] = f"AI 摘要被安全策略拦截或无法生成。原文内容：{item['summary'][:150]}..."
                
        except Exception as e:
            print(f"Gemini API Error for {item['title']}: {e}")
            item['ai_summary'] = "摘要生成失败，可能是内容触发了安全策略或 API 额度超限。请点击链接查看原文。"
        
        processed_list.append(item)
            
    return processed_list
