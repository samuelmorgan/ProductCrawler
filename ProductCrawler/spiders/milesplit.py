# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

from PatrickCrawler.items import PatrickcrawlerItem


class MilesplitSpider(scrapy.Spider):
    name = "milesplit"
    # allowed_domains = ["fl.milesplit.com"]
    counter = 0

    def __init__(self, *args, **kwargs):
        super(MilesplitSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://www.milesplit.com/calendar/2015/cc/all",
            "http://www.milesplit.com/calendar/2015/indoor/all",
            "http://www.milesplit.com/calendar/2015/outdoor/all"
        ]

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//div[contains(@class,"calendar")]//tbody//tr')
        for row in rows:
            item = PatrickcrawlerItem()
            if "/cc/" in response._url:
                item['Type'] = "cc"
            elif "/indoor/" in response._url:
                item['Type'] = "indoor"
            elif "/outdoor/" in response._url:
                item['Type'] = "outdoor"

            item['Date'] = row.xpath('.//span[contains(@class,"dtstart")]/@title').extract()[0].strip().encode('utf-8')
            location = row.xpath('.//td[contains(@class,"location")]//text()').extract()[0].strip()
            arr = location.split(",")
            if len(arr) > 1:
                item['City'] = arr[0]
                item['State'] = arr[1]

            item['Details_URL'] = "http://co.milesplit.com%s" % row.xpath('.//td[contains(@class,"name")]//a[contains(@class,"summary")]/@href').extract()[0].strip()
            try:
                hostedby = row.xpath('.//td[contains(@class,"name")]//div[contains(@class,"caption")]//span//text()').extract()[0].strip()
            except IndexError:
                hostedby = ""

            yield scrapy.Request(
                item['Details_URL'],
                # 'http://tx.milesplit.com/meets/179229-ttfca-meet-of-champions',
                callback=self.parse_details,
                meta={'item': item, 'hostedby': hostedby}
            )

    def parse_details(self, response):
        self.counter += 1
        item = response.meta['item']
        hostedby = response.meta['hostedby']
        sel = Selector(response)

        try:
            rows = sel.xpath('//div[contains(@class,"section")]')
            for row in rows:
                h2_txt = row.xpath('.//h2//text()').extract()[0].strip()
                if h2_txt == 'Additional Information':
                    txt = " ".join(row.xpath('.//text()').extract())
                    arr = txt.split("\r\n")
                    if len(arr) > 3:
                        item['Address'] = arr[2].split(",")[0].strip()
                        if not item['City']:
                            item['City'] = arr[2].split(",")[1].strip()
                        if item['City'] == "High Point":
                            pass
                        if not item['State']:
                            item['State'] = arr[2].split(",")[2].strip()
                        item['Phone_Number'] = arr[3]
                    if item['City'] == "High Point":
                        pass
                    if len(hostedby) > 0:
                        # print ">" * 20
                        # print hostedby
                        xpath_str = '//div[contains(@class,"lining")]//header[contains(@class,"body")]//a[text()="%s"]/@href' % hostedby
                        item['Website_URL'] = sel.xpath(xpath_str).extract()[0].strip()
                    item['Details_URL'] = response._url
        except:
            pass

        return item