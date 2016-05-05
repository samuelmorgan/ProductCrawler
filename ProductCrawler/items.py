# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class PatrickcrawlerItem(scrapy.Item):
    Event_Name = Field()
    Race_Type = Field()
    Date = Field()
    Country = Field()
    City = Field()
    State = Field()
    Location = Field()
    Website_URL = Field()
    Phone_Number = Field()
    Details_URL = Field()
    Facebook_URL = Field()

# class PatrickcrawlerItem(scrapy.Item):
#     Type = Field()
#     Date = Field()
#     City = Field()
#     State = Field()
#     Address = Field()
#     Website_URL = Field()
#     Phone_Number = Field()
#     Details_URL = Field()
