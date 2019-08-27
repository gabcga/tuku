# -*- coding: utf-8 -*-
import scrapy
import requests
import os



class TukuspiderSpider(scrapy.Spider):
    name = 'tukuspider'
    allowed_domains = ['www.tuku.cc']
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    input = input('comic number:')
    try:
        start_urls = ['http://www.tuku.cc/comic/'+str(input)]
    except IOError :
        print('wrong comic number')


    def parse(self, response):
        list = response.css('div[id="chapterlistload"]').css('a::attr(href)').extract()
        urls = ['http://www.tuku.cc'+l for l in list]
        #print(urls)
        for url in urls:
            #print(url)
            yield scrapy.Request(url, meta={'chapter': url.split('/')[-2], 'page': 0}, callback=self.parse_chapter_contents)


    def parse_chapter_contents(self, response):
        print(response.url)

        img_url = response.css('img[id="cp_image"]::attr(src)').extract()[0]
        page = response.meta['page']
        chapter = 'qilongzhu/'+response.meta['chapter']
        #print(next)
        #print(img_url)
        if not os.path.exists(chapter):
            os.mkdir(chapter)

        if requests.get(img_url).status_code == 200:
            with open(os.path.join(chapter, str(page)+'.jpg'), 'wb') as imgf:
                imgf.write(requests.get(img_url).content)
            next = 'http://www.tuku.cc' + response.css('a[href*="/p"]::attr(href)').extract()[-1]
            yield scrapy.Request(next, meta={'chapter': response.meta['chapter'], 'page': page + 1},
                                   callback=self.parse_chapter_contents)

        else:
            print('chapter download finished: ' + response.meta['chapter'])
        #print('download finished ' + response.meta['title'])








