# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class ShkolaSpider(scrapy.Spider):
    name = 'shkola'
    start_urls = ['https://shkola.ua/']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src")
        all_text = response.xpath(
            "//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")
        yield {
            'url': response.url,
            'payload': [{'type': 'text', 'data': text.get().strip()} for text in all_text] +
                       [{'type': 'image', 'data': image.get()} for image in all_images]
        }
        n = response.url == self.start_urls[0]
        if response.url == self.start_urls[0]:
            all_links = response.xpath(
                "//a/@href[starts-with(., '/')]")
            selected_links = [link.get() for link in all_links][:19]
            for link in selected_links:
                yield scrapy.Request('https://shkola.ua' + link, self.parse)
