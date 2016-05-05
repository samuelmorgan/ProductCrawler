# -*- coding: utf-8 -*-

# Scrapy settings for PatrickCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'PatrickCrawler'

SPIDER_MODULES = ['PatrickCrawler.spiders']
NEWSPIDER_MODULE = 'PatrickCrawler.spiders'
DEPTH_LIMIT = 5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PatrickCrawler (+http://www.yourdomain.com)'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(BASE_DIR)

FEED_EXPORTERS = {
    'csv': 'PatrickCrawler.feedexport.MyProjectCsvItemExporter'
}

FIELDS_TO_EXPORT = [
    'Event_Name',
    'Race_Type',
    'Date',
    'Country',
    'City',
    'State',
    'Location',
    'Website_URL',
    'Phone_Number',
    'Details_URL',
    'Facebook_URL',
]


# FIELDS_TO_EXPORT = [
#     'Type',
#     'Date',
#     'City',
#     'State',
#     'Address',
#     'Website_URL',
#     'Phone_Number',
#     'Details_URL',
# ]

CSV_DELIMITER = ","