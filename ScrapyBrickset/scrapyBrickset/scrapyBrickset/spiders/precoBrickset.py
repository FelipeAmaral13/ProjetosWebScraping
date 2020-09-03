# -*- coding: utf-8 -*-
import scrapy
from scrapyBrickset.items import ScrapybricksetItem

class PrecobricksetSpider(scrapy.Spider):
    name = 'precoBrickset'
    allowed_domains = ['https://brickset.com/sets/year-2020']
    start_urls = ['https://brickset.com/sets/year-2020']

    def parse(self, response):
        item = ScrapybricksetItem()

        for nomes in response.xpath('//article[@class="set"]'):
            item['name'] = nomes.xpath('.//div[@class="meta"]/h1/a/text()').extract_first()
            item['preco'] = nomes.xpath('.//div[@class="meta"]/div[@class="col"]/dl/dd[3]/text()').extract_first()

            yield item


        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).get()
        if next_page is not None:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )