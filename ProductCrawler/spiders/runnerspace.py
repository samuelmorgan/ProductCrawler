# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

from PatrickCrawler.items import PatrickcrawlerItem


class RunnerspaceSpider(scrapy.Spider):
    name = "runnerspace"
    # allowed_domains = [".runnerspace.com"]
    counter = 0

    def __init__(self, *args, **kwargs):
        super(RunnerspaceSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://roads.runnerspace.com/gprofile.php?do=events&mgroup_id=90&year=2015&month=%d&list=1" % d for d in range(4, 13, 1)
        ]

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//div[contains(@class,"album_block")]//tr[contains(@class,"MC_ajax_edit_wrapper")]')
        for row in rows:
            item = PatrickcrawlerItem()
            try:
                item['Event_Name'] = row.xpath('.//a[contains(@class,"MC_ajax_return_title")]//text()').extract()[0].encode('utf-8')
            except IndexError:
                continue
            item['Details_URL'] = row.xpath('.//a[contains(@class,"MC_ajax_return_title")]/@href').extract()[0].encode('utf-8')

            item['Race_Type'] = ''
            item['Date'] = ''
            item['City'] = ''
            item['State'] = ''
            item['Country'] = ''
            item['Location'] = ''
            item['Website_URL'] = ''
            item['Phone_Number'] = ''
            item['Facebook_URL'] = ''

            yield scrapy.Request(
                item['Details_URL'],
                # 'http://www.runnerspace.com/eprofile.php?event_id=5358',
                callback=self.parse_details,
                meta={'item': item}
            )

    def parse_details(self, response):
        self.counter += 1
        item = response.meta['item']
        sel = Selector(response)
        if len(sel.xpath('//div[@id="minimeevent"]')) < 1:
            print ">" * 20
            return item

        rows = sel.xpath('//div[@id="minimeevent"]//div[contains(@class,"eventbody")]//tr')
        for row in rows:
            txt = row.xpath('.//td//text()').extract()
            if "Sport:" in txt:
                item['Race_Type'] = txt[1].encode('utf-8')
                break
        try:
            item['Website_URL'] = sel.xpath('//div[@id="minimeevent"]//div[contains(@class,"eventbody")]//a[text()="Click here"]/@href').extract()[0].encode('utf-8')
        except:
            pass
        try:
            txt = ' '.join(sel.xpath('//div[@id="header_info"]//text()').extract()).strip().encode('utf-8')
            arr = txt.split(" ")
            item['Date'] = "%s %s %s" % (arr[0], arr[1], arr[2])
            txt = txt.replace(item['Date'], '').strip()
            arr = txt.split(",")
            if len(arr) > 2:
                item['Country'] = arr[2].encode('utf-8')
                item['State'] = arr[1].encode('utf-8')
                item['City'] = arr[0].encode('utf-8')
            elif len(arr) == 2:
                item['Country'] = arr[1].encode('utf-8')
                item['City'] = arr[0].encode('utf-8')
        except:
            pass
        try:
            hrefs = sel.xpath('//div[@id="header_info"]//a/@href').extract()
            for href in hrefs:
                if "facebook.com" in href:
                    item['Facebook_URL'] = href
        except:
            pass

        return item