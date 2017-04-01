'''
Finds all profile page URLs of a steam community group
author: Karl Thornton <karl.genockey.thornton@gmail.com
https://kaijento.github.io/2017/04/01/web-scraping-steamcommunity.com/
'''

import scrapy

group = 'KeyVendorNet'

class SteamCommunity(scrapy.Spider):
    name = 'Steam Community'

    base_url = 'http://steamcommunity.com/groups/{}/members/'.format(group)
    base_url += '?p={}'

    start_urls = [
        base_url.format(1)
    ]

    def parse(self, response):
        last_page = response.css('.pagelink::text').extract()[-1]
        for n in range(1, int(last_page) + 1):
            yield scrapy.Request(
                self.base_url.format(n), callback=self.extract_members)

    def extract_members(self, response):
        for href in response.css('.linkFriend::attr(href)'):
            yield { 'href': href.extract() }
