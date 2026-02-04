from fetcher import fetch_news
from processor import process_news
from mailer import send_email
import time

def main():
    print("Step 1: Fetching news from sources...")
    raw_news = fetch_news()
    
    print("Step 2: Processing news with Gemini AI (Summarization & Translation)...")
    processed_news = process_news(raw_news)
    
    print("Step 3: Sending daily email...")
    send_email(processed_news)
    
    print("Daily task completed!")

if __name__ == "__main__":
    main()
