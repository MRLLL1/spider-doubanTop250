# -*- coding: utf-8 -*-
import scrapy
from doubanmovie.items import DoubanmovieItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    url = 'https://movie.douban.com/top250?start='
    page = 0
    start_urls = [url+str(page)]

    def parse(self, response):
        info_list = response.xpath('//div[@class="info"]')
        for data in info_list:
            item = DoubanmovieItem()
            item['name'] = data.xpath('./div[@class="hd"]/a/span[1]/text()').extract()[0].encode('utf-8')
            item['actor'] = data.xpath('./div[@class="bd"]/p[1]/text()').extract()[0].strip().encode('utf-8')
            item['rating'] = data.xpath('./div//div/span[@class="rating_num"]/text()').extract()[0].encode('utf-8')
            infos = data.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if len(infos)!=0:
                infos = infos[0].strip().encode('utf-8')
            else:
                infos = ' '
            item['info'] = infos
            yield item

        if self.page<225:
            self.page+=25
            yield scrapy.Request(self.url+str(self.page), callback=self.parse)
