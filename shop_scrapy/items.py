# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    jan = scrapy.Field()
    url = scrapy.Field()
