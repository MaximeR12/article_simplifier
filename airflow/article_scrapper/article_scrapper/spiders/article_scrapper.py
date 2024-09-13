import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from ..items import ArticleScrapperItem
from .utils import text_cleaner


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
                'fields': ['main_txt'],}
        }
    }

    rules = (
        Rule(LinkExtractor(restrict_css=".fig-ensemble__first-article-link"), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = ArticleScrapperItem()
        txt_raw = response.css('.fig-paragraph').getall()
        txt_cleaned = text_cleaner(txt_raw)
        item["main_txt"] = txt_cleaned
        yield item
