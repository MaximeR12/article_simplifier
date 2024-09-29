import os
import requests
import logging
import sqlite3
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from ..items import ArticleScrapperItem
from .utils import text_cleaner

# def send_article_to_db(item):
#     # Use the DB_API_URL and DB_API_TOKEN from environment variables
#     db_api_url = os.getenv("DB_API_URL")
#     db_api_token = os.getenv("DB_API_TOKEN")

#     # Create a dictionary with the item data
#     article_data = {
#         "source": "figaro",
#         "title": item.get("title", ""),
#         "content": item.get("main_txt", ""),
#         "language": "fr",
#     }

#     # Send the article data to the DB API
#     response = requests.post(
#         f"{db_api_url}/article/",
#         json=article_data,
#         headers={"x-token": db_api_token}
#     )
#     if response.status_code == 200:
#         logging.info("Article sent to DB")
#     else:
#         logging.error("Failed to send article to DB")
def insert_article_to_sqlite(article):
    conn = sqlite3.connect('/opt/airflow/airflow.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scraping_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        title TEXT,
        content TEXT,
        language TEXT
    )
    ''')
    
    # Insert data
    cursor.execute('''
    INSERT INTO scraping_articles (source, title, content, language) 
    VALUES (?, ?, ?, ?)
    ''', ("Scraping_figaro", article['title'], article['main_txt'], "fr"))
    
    conn.commit()
    conn.close()


class FigaroSpider(CrawlSpider):
    name = 'figarospider'
    allowed_domains = ['lefigaro.fr']
    start_urls = ['https://www.lefigaro.fr/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        'FEEDS': {
            '../data/articles.csv': {
                'format': 'csv',
                'fields': ['title', 'main_txt'],}
        }
    }

    rules = (
        Rule(LinkExtractor(restrict_css=".fig-ensemble__first-article-link"), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = ArticleScrapperItem()
        item["title"] = response.css('h1.fig-headline.fig-pagination__hidden::text').get().strip()  # Extract the title from the h1 element
        txt_raw = response.css('.fig-paragraph').getall()
        txt_cleaned = text_cleaner(txt_raw)
        item["main_txt"] = txt_cleaned
        insert_article_to_sqlite(item)
        yield item