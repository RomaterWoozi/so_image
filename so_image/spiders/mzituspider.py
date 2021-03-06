# -*- coding: utf-8 -*-
import scrapy

from so_image.items import SoImageItem


class MZiTuSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/all']

    def parse(self, response):
        ebook_item = SoImageItem()
        data = []
        for earch in response.xpath("//ul[@class='archives']"):
            item = {}
            print((earch.xpath("./preceding::*[1]/text()").extract()[0]))
            item['year'] = " %s" % (earch.xpath("./preceding::*[1]/text()").extract()[0])
            alink_list = []
            for liitem in earch.xpath("./li"):
                pList = []
                for ptemp in liitem.xpath("./p[@class='url']/a"):
                    pdata = {'name': ptemp.xpath("./text()").extract()[0], 'alink': ptemp.xpath("./@href").extract()[0]}
                    pList.append(pdata)
                    yield scrapy.Request(pdata['alink'], callback=self.parse_subpage)
                temp = {'month': liitem.xpath("./p[@class='month']/em/text()").extract()[0], 'columns': pList}
                alink_list.append(temp)
            item['alink_list'] = alink_list
            data.append(item)

        ebook_item['data_list'] = data
        yield ebook_item
        pass

    def parse_subpage(self, response):
        image_lists = []
        if ("下一页" in response.xpath(
                "//div[@class='pagenavi']/a[last()]/span/text()").extract()[0]):
            next_page = response.xpath("//div[@class='pagenavi']/a[last()]/@href").extract()[0]
            # 获取图片路径
            for item in response.xpath("//div[@class='main-image']"):
                image_lists.append(item.xpath("./p/a/img/@src").extract()[0])
            yield {'image_urls': image_lists, 'referer': response.url}
            yield scrapy.Request(next_page, callback=self.parse_subpage)
        pass
