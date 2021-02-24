import datetime

import PyPDF2
import requests
import scrapy
import pandas as pd

from ..items import SavenowItem


class SavenowSpider(scrapy.Spider):
    name = 'savenow'

    def start_requests(self):
        start_urls = [
            'https://ipaam.com.vn/vi/quy-dau-tu/quy-mo-co-phieu-vndaf/bao-cao-nav/',
            'https://dcvfm.com.vn/quy-dau-tu-chung-khoan-viet-nam-vfmvf1/vf1-thong-tin-ve-quy/',
            'https://dcvfm.com.vn/quy-dau-tu-trai-phieu-viet-nam-vfmvfb/vfb-thong-tin-ve-quy-mo/',
            'https://dcvfm.com.vn/quy-hoan-doi-danh-muc-etf-vfmvn30/etf-thong-tin-ve-quy/',
            'https://baovietfund.com.vn/san-pham/BVBF',
            'https://baovietfund.com.vn/san-pham/BVPF',
            'https://www.ssi.com.vn/ssiam/hieu-qua-dau-tu-cua-quy-ssi-sca',
            'https://wm.vinacapital.com/quy-dau-tu-trai-phieu-bao-thinh-vff',
            'http://www.vietinbankcapital.vn/vi-vn/san-pham-dich-vu/san-pham/504/PRODUCT_INFO/F2',
            'http://www.techcomcapital.com.vn/index.php/category/quan-he-ndt/cong-bo-thong-tin/']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        if str(response.url).find('vndaf', 0) > 0:
            all_listings = response.xpath('//*[@id="1582875613813-6c2dd926-ebee"]')
            for tesla in all_listings:
                link = tesla.css('h5').css('a::attr(href)').get()
                #print(tesla.get())
                yield scrapy.Request(link, callback=self.download_file)
        elif str(response.url).find('vf1', 0) > 0:
            all_listings = response.xpath('(//*[@id="fund-pages"]//div//div[@class="element"])[1]')
            for tesla in all_listings:
                tbody = tesla.css('strong::text').getall()[1]
                item = SavenowItem()
                item['name'] = 'VFMVF1'
                item['date'] = str(tesla.css('span::text').get()).replace(' ', '')[7:]
                item['value'] = str(tbody).replace('.', '').replace(',', '.')

                yield item
        elif str(response.url).find('vfb', 0) > 0:
            all_listings = response.xpath('(//*[@id="fund-pages"]//div//div[@class="element"])[1]')

            for tesla in all_listings:
                tbody = tesla.css('strong::text').getall()[1]
                item = SavenowItem()
                item['name'] = 'VFMVFB'
                item['date'] = str(tesla.css('span::text').get()).replace(' ', '')[7:]
                item['value'] = str(tbody).replace('.', '').replace(',', '.')

                yield item
        elif str(response.url).find('vfmvn30', 0) > 0:
            all_listings = response.xpath('(//*[@id="fund-pages"]//div//div[@class="element"])[1]')
            for tesla in all_listings:
                tbody = tesla.css('strong::text').getall()[1]
                item = SavenowItem()
                item['name'] = 'EFTVN30'
                item['date'] = str(tesla.css('span::text').get()).replace(' ', '')[7:]
                item['value'] = str(tbody).replace('.', '').replace(',', '.')

                yield item
        elif str(response.url).find('BVBF', 0) > 0:
            all_listings = response.xpath('//*[@id="main-content"]/div[2]/div[1]/div/div/div/div[2]/ul/li[1]')

            for tesla in all_listings:
                tbody = tesla.css('strong::text').get()
                item = SavenowItem()
                item['name'] = 'BVBF'
                item['date'] = str(tesla.css('li::text').get())[18: 28]
                item['value'] = str(tbody).replace('.', '').replace(' VNĐ', '')

                yield item
        elif str(response.url).find('BVPF', 0) > 0:
            all_listings = response.xpath('//*[@id="main-content"]/div[2]/div[1]/div/div/div/div[2]/ul/li[1]')

            for tesla in all_listings:
                tbody = tesla.css('strong::text').get()
                item = SavenowItem()
                item['name'] = 'BVPF'
                item['date'] = str(tesla.css('li::text').get())[18: 28]
                item['value'] = str(tbody).replace('.', '').replace(' VNĐ', '')

                yield item
        elif str(response.url).find('sca', 0) > 0:
            all_listings = response.xpath('/html/body/main/section[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div')
            date = response.xpath('/html/body/main/section[2]/div/div/div[2]/div[2]/div/div/div[1]/div/span[2]/text()')
            for tesla in all_listings:
                item = SavenowItem()
                item['name'] = 'SCA'
                item['date'] = date.get().replace('\n', '').replace(' ', '')[-10:]
                item['value'] = str(tesla.css('::text').get()).replace('.', '').replace(',', '.').replace('\n',
                                                                                                          '').replace(
                    ' ', '')
                yield item
        elif str(response.url).find('vff', 0) > 0:
            value = response.xpath('//*[@id="ket-qua-hd-quy"]/div/div[6]/table/tbody/tr[1]/td[1]/strong')
            date = response.xpath('//*[@id="ket-qua-hd-quy"]/div/div[6]/table/tbody/tr[1]/td[1]/small/text()')
            item = SavenowItem()
            item['name'] = 'VFF'
            item['date'] = date.get().replace('\n', '').replace(' ', '')[-10:]
            item['value'] = str(value.css('::text').get())  # .replace('\n','').replace(' ', '')

            yield item
        elif str(response.url).find('vietinbankcapital', 0) > 0:
            report = response.xpath('//*[@id="listObj"]/div[1]')
            li = report.xpath('//ul[@class="dec"]')
            for tesla in li:
                a = tesla.xpath('//li[@class="one animated fadeInUp"]/span')
                b = a.xpath('//a[contains(text(),"Báo cáo NAV quỹ VTBF tuần từ")]')
                link = 'http://www.vietinbankcapital.vn/vi-vn/' + b.css('a::attr(href)').get()

                yield scrapy.Request(link, callback=self.treat_vtbf)
        elif str(response.url).find('techcomcapital', 0) > 0:
            report = response.xpath('//*[@id="content"]')
            a = report.xpath('//a[contains(text(),"TCBF_BC_Ngay")]')
            link = a.css('a::attr(href)').get()
            yield scrapy.Request(link, callback=self.download_fileTCBF)

    def treat_vtbf(self, response):
        value = response.xpath(
            '/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div[2]/table/tbody/tr[3]/td[4]/text()[1]')
        date = response.xpath(
            '/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div[2]/text()[4]')
        item = SavenowItem()

        item['name'] = 'VTBF'
        item['date'] = str(date.get()).replace('\n', '')[-10:]
        item['value'] = str(value.get()).replace(' ', '').replace(u'\xa0', u'').replace(',', '')

        yield item

    def download_fileTCBF(self, response):
        r = requests.get(response.url, stream=True)

        with open('TCBF.xlsx', 'wb') as fd:
            for chunk in r.iter_content(2000):
                fd.write(chunk)

        yield self.readTCBF()

    def download_file(self, response):
        r = requests.get(response.url, stream=True)

        with open('VNDAF.pdf', 'wb') as fd:
            for chunk in r.iter_content(2000):
                fd.write(chunk)

        yield self.readVNDAF()

    def readVNDAF(self):
        # creating a pdf file object
        pdfFileObj = open('VNDAF.pdf', 'rb')

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # creating a page object
        pageObj = pdfReader.getPage(0)

        # extracting text from page
        text = pageObj.extractText().encode('utf-8', errors='ignore')

        text = str(text).replace("\n", "").replace("\\", "").replace('n', '')
        value = text.index("(NAV/Uit)", 0)
        value2 = text.index("NAV/UNIT AS OF", 0)

        item = SavenowItem()
        item['name'] = 'VNDAF'
        item['date'] = str(text[value2 + 15: value2 + 25])
        item['value'] = str(text[value + 10:value + 19]).replace(',', '')

        pdfFileObj.close()
        return item

    def readTCBF(self):
        data = pd.read_excel('TCBF.xlsx', usecols=['Unnamed: 1','Unnamed: 2','Unnamed: 3'])
        date_time_str = str(data.iloc[12]['Unnamed: 2'])[0:10]
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        item = SavenowItem()
        item['name'] = 'TCBF'
        item['value'] = data.iloc[18]['Unnamed: 3']
        item['date'] = date_time_obj.strftime("%d/%m/%Y")

        return item
