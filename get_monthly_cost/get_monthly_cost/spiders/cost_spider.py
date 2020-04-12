import scrapy
from scrapy_splash import SplashRequest
from get_monthly_cost.items import TutorialItem
import json
import time

class QuotesSpider(scrapy.Spider):
    name = "cost"
    # Example home page: https://www.zillow.com/homedetails/6819-Verandah-Way-Irving-TX-75039/2084390867_zpid/
    home_page = 'https://www.zillow.com/homedetails/'

    start_urls = []

    def __init__(self):
        with open('../data/zestimate.json', 'r') as f:
            self.id = 0
            self.zestimate = json.loads(f.read())
            for house in self.zestimate:
                # Get the address and replace blank with _
                address = house['address']
                address_for_url = address.replace(' ', '-').replace(',','')
                # Get zpid
                zpid = house['zpid'] 
                self.start_urls.append(self.home_page + address_for_url + '/' + zpid + '_zpid')
                #self.start_urls = self.start_urls[0:1]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'timeout': 60, 'wait': 3})

    def parse(self, response):
        try:
	    monthly_cost = response.xpath('//*[@id="ds-container"]/div[4]/div[1]/div/div[4]/div/span[2]/text()').getall()
            monthly_cost = monthly_cost[0]
            monthly_cost = monthly_cost.replace('$','').replace(',','')
            house = self.zestimate[self.id]
            house['cost'] = monthly_cost
            item = TutorialItem()
            item = house
            yield item
        except Exception as e:
            print (e)
        
        print(self.start_urls[self.id])
        print(monthly_cost)
        self.id = self.id + 1
