import scrapy


class PigpriceSpider(scrapy.Spider):
    name = "pigprice"
    start_urls = [
        'http://hqb.nxin.com/hqb/queryPigPrice.shtml',
    ]

    def parse(self, response):

        for district in response.css('table tbody tr'):
            yield {
                'districtName': district.css("td::text")[0].extract(),
                'districtData': district.css("td span::text").extract(),
                'priceDate': response.css("div.pt_tit::text").extract_first(),
            }
