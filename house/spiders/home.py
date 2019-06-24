# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from house.items import HouseItem,esfHouseItem


class HomeSpider(CrawlSpider):
    name = 'home'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']
    #redis_key = "house"
    rules = (
        #匹配全国的地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='onCont']//tr",)),follow=True),
        #匹配新房
        Rule(LinkExtractor(restrict_xpaths=("//div[@track-id='newhouse']//div[@class='s4Box']",)),follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='nlcd_name']/a",)),callback='parse_newhouse'),

        # # 列表页翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='page']",)), follow=True),
        #匹配二手房
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='s1']/a[2]",)), callback= "parse_tail",follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//dl[@class='clearfix']//h4/a",)), callback="parse_esf"),
        # 列表页翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='page_al']//a",)), follow=True),
    )

    #新房的解析
    def parse_newhouse(self, response):

        nlcd_name = response.xpath("//div[@class='tit']/h1//text()").get()
        new_house_address = response.xpath("//div[@class='br_left']//li[2]//text()").get()+\
                            response.xpath("//div[@class='br_left']//li[3]//text()").get()
        residence = response.xpath("//div[@class='biaoqian1']/a[1]/text()").get()
        new_disk = response.xpath("//div[@class='biaoqian1']/a[2]/text()").get()
        avg_money = response.xpath("//div[@class='inf_left fl ']//text()").getall()
        avg_money = ''.join(list(map(lambda avg:re.sub('\s','',avg) ,avg_money)))
        housewear = response.xpath("//div[@class='fl zlhx']//text()").getall()
        housewear = list(map(lambda ware: re.sub('\s', '', ware), housewear))
        housewear = ','.join([i for i in housewear if len(i) > 0])
        project_addr = response.xpath("//div[@class='information_li']//span/text()").get()
        open_time = response.xpath("//div[@class='inf_left fl']//a[@class='kaipan']/text()").get()
        item = HouseItem(
            nlcd_name = nlcd_name ,
            new_house_address = new_house_address,
            residence = residence,
            new_disk = new_disk,
            avg_money = avg_money,
            housewear = housewear,
            project_addr = project_addr,
            open_time = open_time
        )
        print("tong" ,nlcd_name)
        yield item
        def parse_tail(self, response):
            item1 = {}
            item1["area"] = response.xpath(
            "//div[@class='screen_al']//ul[contains(@class,'choose_screen ')]/li/a/text()").get()
        # print(item1)

    def parse_esf(self, response):
        city = response.xpath("//div[@class='bread']/a[2]/text()").get()
        country = response.xpath("//div[@class='bread']/a[3]/text()").get()
        nlcd_name = response.xpath("//div[contains(@class,'title')]//h1/text()").extract_first().strip()
        infos = response.xpath("//div[@class='tt']/text()").extract()
        infos = list(map(lambda x: re.sub('\s', '', x), infos))
        item = esfHouseItem(city=city, nlcd_name=nlcd_name, infos=infos, country=country)
        yield item

