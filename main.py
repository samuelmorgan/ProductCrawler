from scrapy import cmdline


cmdline.execute("scrapy crawl runnerspace -o runnerspace_items.csv".split())
# cmdline.execute("scrapy crawl milesplit -o milesplit_items.csv".split())