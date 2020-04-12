import scrapy
from get_address.items import TutorialItem
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    home_page = 'https://www.zillow.com/'
    search_location = 'dallas-tx/'
    current_page_pattern = '22currentPage%22:{0}'
    search_criteria = '?searchQueryState={%22pagination%22:{%22currentPage%22:1},%22mapBounds%22:{%22west%22:-97.06170224023435,%22east%22:-96.47805355859373,%22south%22:32.648110266273044,%22north%22:33.006998422969524},%22regionSelection%22:[{%22regionId%22:38128,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:11,%22filterState%22:{%22price%22:{%22max%22:500000},%22monthlyPayment%22:{%22max%22:1938}},%22isListVisible%22:true}'

    start_urls = [home_page + search_location + search_criteria]

    def parse(self, response):
        addresses = response.xpath('/html/body/div[1]/div[6]/div/div[1]/div[1]/div[1]/ul/li/article/div[1]/a/address/text()').getall()
        for addr in addresses:
            item = TutorialItem()
            item['addr'] = addr
            yield item

        next_page = response.css('#mobile-pagination-root > div > ol > li.zsg-pagination-next > a::attr(href)').get()
        if next_page is not None:
            next_page_str = next_page.split('/')[-2]
            next_page_num = re.findall(r'\d+', next_page_str)[0]
	    next_page_url = response.urljoin(next_page_str)+'/'+self.search_criteria.replace('%22currentPage%22:1',self.current_page_pattern.format(next_page_num))     
            yield scrapy.Request(next_page_url, callback=self.parse)
