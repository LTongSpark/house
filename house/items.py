# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #新房名字
    nlcd_name = scrapy.Field()
    #新房地址
    new_house_address = scrapy.Field()
    residence = scrapy.Field()
    new_disk = scrapy.Field()
    avg_money = scrapy.Field()
    housewear = scrapy.Field()
    project_addr = scrapy.Field()
    open_time = scrapy.Field()

class esfHouseItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    # 新房名字
    nlcd_name = scrapy.Field()
    # 新房地址
    city = scrapy.Field()
    country = scrapy.Field()
    infos = scrapy.Field()