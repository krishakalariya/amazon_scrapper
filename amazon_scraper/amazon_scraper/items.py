# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScraperItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    reviews = scrapy.Field()
    model_name = scrapy.Field()

