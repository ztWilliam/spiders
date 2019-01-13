import scrapy
import json
import os

'''
从行情宝拉取当天的猪价行情（具体到各地级市）
每个省输出一个json文件。
'''
class PigpriceDetailSpider(scrapy.Spider):
    name = "pigpriceDetail"
    start_urls = [
        # 上海
        'http://hqb.nxin.com/hqb/areapriceinfo-1.shtml',
        # 云南
        'http://hqb.nxin.com/hqb/areapriceinfo-237.shtml',
        # 内蒙古
        'http://hqb.nxin.com/hqb/areapriceinfo-1815.shtml',
        # 北京
        'http://hqb.nxin.com/hqb/areapriceinfo-3475.shtml',
        # 吉林
        'http://hqb.nxin.com/hqb/areapriceinfo-3815.shtml',
        # 四川
        'http://hqb.nxin.com/hqb/areapriceinfo-4771.shtml',
        # 天津
        'http://hqb.nxin.com/hqb/areapriceinfo-9684.shtml',
        # 宁夏
        'http://hqb.nxin.com/hqb/areapriceinfo-9947.shtml',
        # 安徽
        'http://hqb.nxin.com/hqb/areapriceinfo-10215.shtml',
        # 山东
        'http://hqb.nxin.com/hqb/areapriceinfo-11966.shtml',
        # 山西
        'http://hqb.nxin.com/hqb/areapriceinfo-14059.shtml',
        # 广东
        'http://hqb.nxin.com/hqb/areapriceinfo-15591.shtml',
        # 广西
        'http://hqb.nxin.com/hqb/areapriceinfo-17313.shtml',
        # 新疆
        'http://hqb.nxin.com/hqb/areapriceinfo-18757.shtml',
        # 江苏
        'http://hqb.nxin.com/hqb/areapriceinfo-19840.shtml',
        # 江西
        'http://hqb.nxin.com/hqb/areapriceinfo-21395.shtml',
        # 河北
        'http://hqb.nxin.com/hqb/areapriceinfo-23078.shtml',
        # 河南
        'http://hqb.nxin.com/hqb/areapriceinfo-25475.shtml',
        # 浙江
        'http://hqb.nxin.com/hqb/areapriceinfo-28009.shtml',
        # 海南
        'http://hqb.nxin.com/hqb/areapriceinfo-29627.shtml',
        # 湖北
        'http://hqb.nxin.com/hqb/areapriceinfo-29887.shtml',
        # 湖南
        'http://hqb.nxin.com/hqb/areapriceinfo-31233.shtml',
        # 甘肃
        'http://hqb.nxin.com/hqb/areapriceinfo-33784.shtml',
        # 福建
        'http://hqb.nxin.com/hqb/areapriceinfo-35288.shtml',
        # 西藏
        'http://hqb.nxin.com/hqb/areapriceinfo-36492.shtml',
        # 贵州
        'http://hqb.nxin.com/hqb/areapriceinfo-37257.shtml',
        # 辽宁
        'http://hqb.nxin.com/hqb/areapriceinfo-38897.shtml',
        # 重庆
        'http://hqb.nxin.com/hqb/areapriceinfo-40518.shtml',
        # 陕西
        'http://hqb.nxin.com/hqb/areapriceinfo-41593.shtml',
        # 青海
        'http://hqb.nxin.com/hqb/areapriceinfo-43459.shtml',
        # 黑龙江
        'http://hqb.nxin.com/hqb/areapriceinfo-43919.shtml',
    ]

    def parse(self, response):
        dist = getattr(self, 'dist', '')
        
        if dist != '':
            os.makedirs(dist, 0o777, True)

        datePart = response.css("div.pt_tit::text").extract()
        priceDate = datePart[len(datePart) - 1]

        parentPart = response.css("div.pt_tit em::text").extract_first().split('\n\t')[
            1].split('\t')
        parentName = parentPart[len(parentPart) - 1]

        districts = response.css('table tbody tr')
        subData = []
        i = 0
        while i < len(districts) - 1:
            district = districts[i]
            if district is not None:
                item = {
                    "name": district.css("td::text")[0].extract(),
                    "data": district.css("td span::text").extract(),
                }
                subData.append(item)

            i = i + 1

        data = {
            "parentArea": parentName,
            "priceDate": priceDate,
            "children": subData
        }

        yield {
            "parentArea": parentName,
            "priceDate": priceDate,
            "children": subData
        }

        # 将data输出到json文件中, 若传入dist参数, 则将文件放到指定目录中
        fileName = 'pigprice-%s-%s.json' % (priceDate, parentName) 
        if dist != '':
            fileName = dist + '/' + fileName

        self.writeToFile(fileName, data)

    def writeToFile(self, fileName, jsonable):
        if os.path.exists(fileName):
            os.remove(fileName)

        with open(fileName, 'wt') as f:
            f.write(json.dumps(jsonable))
