# vnexpress.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_vnexpress_news():
    url = "https://vnexpress.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    articles = soup.find_all("article", {"class": "item-news"})
    data = []
    
    for article in articles:
        title = article.find("h3").text.strip()
        link = article.find("a")["href"]
        summary = article.find("p").text.strip()
        data.append({"title": title, "link": link, "summary": summary})
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    news_data = crawl_vnexpress_news()
    print(news_data.head())
    news_data.to_csv("vnexpress_news.csv", index=False)
    print("Data saved to vnexpress_news.csv")