# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class TennismagSpider(scrapy.Spider):
    name = 'tennismag'
    start_urls = ['https://tennismag.com.ua/catalog/raketki/']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'row bxr-list')]/div[starts-with(@id, 'bx')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//div[@class='bxr-element-name']/a/@title").get(),
                'price': product.xpath(".//span[starts-with(@class, 'bxr-market-current-price')]/text()").get(),
                'img': 'https://tennismag.com.ua' + product.xpath(".//div[@class='bxr-element-image']/a/img/@src").get()
            }
