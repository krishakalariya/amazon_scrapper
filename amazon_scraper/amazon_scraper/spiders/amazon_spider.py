from urllib.parse import urljoin
import pandas as pd
import scrapy
from scrapy_splash import SplashRequest


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=ipad"]

    def __init__(self):
        super(AmazonSpiderSpider, self).__init__()
        self.data = []

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        product_links = response.xpath('//a[@class="a-link-normal s-no-outline"]/@href').extract()
        print('products', product_links)
        i = 0
        for product_link in product_links:
            absolute_url = urljoin(response.url, product_link.split("?")[0])
            print('abs', absolute_url)
            i += 1
            print('i', i)
            yield scrapy.Request(absolute_url, callback=self.parse_product)

        # Pagination
        next_page_relative_url = response.css('a.s-pagination-next::attr(href)').get()
        next_page_url = urljoin(response.url, next_page_relative_url)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        # scrap product details.
        product_title = response.css('#productTitle').xpath('text()').get()
        product_image = response.css('img#landingImage::attr(src)').get()
        product_price = response.xpath('//span[@class="a-price-whole"]/text()').get()
        reviews = response.xpath('//span[@id="acrPopover"]//span[@class="a-icon-alt"]/text()').get()
        model_name = response.xpath(
            '//tr[@class="a-spacing-small po-model_name"]//td[@class="a-span9"]/span[@class="a-size-base po-break-word"]/text()').get()
        data_item = {
            'title': product_title.strip(),
            'image': product_image,
            'price': product_price,
            'reviews': reviews,
            'model_name': model_name
        }
        self.data.append(data_item)
        yield data_item

    def closed(self, reason):
        df = pd.DataFrame(self.data)
        df.to_excel('data.xlsx', index=True)
