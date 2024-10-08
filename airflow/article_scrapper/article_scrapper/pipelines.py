# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ArticleScrapperPipeline:
    def process_item(self, item, spider):
        # Ensure the item matches the structure expected by the database
        formatted_item = {
            "source": spider.name,
            "title": item.get("title", ""),
            "content": item.get("main_txt", ""),
            "language": item.get("language", "fr"),
        }
        return formatted_item
