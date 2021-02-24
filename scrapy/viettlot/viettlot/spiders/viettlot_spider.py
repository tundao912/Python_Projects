import scrapy

from ..items import ViettlotItem


class ViettlotSpider(scrapy.Spider):
    name = "viettlot"

    def start_requests(self):
        ky_quay = 2
        urls = ['https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/645?id=00001&nocatche=1']

        while ky_quay < 10:
            ky_quayStr = str(ky_quay).zfill(5)
            start_url = 'https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/645?id={}&nocatche=1'.format(ky_quayStr)
            urls.append(start_url)
            ky_quay = ky_quay + 1
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response, **kwargs):
        data = response.xpath('//*[@id="divLeftContent"]')
        for tesla in data:
            ky_quay_chitiet = tesla.css('h5').css('b::text').getall()
            ky_quay_so = str(ky_quay_chitiet[0])[1:]
            ky_quay_ngay = ky_quay_chitiet[1]

            ket_qua = tesla.css('span.bong_tron::text').getall()
            ket_qua_01 = ket_qua[0]
            ket_qua_02 = ket_qua[1]
            ket_qua_03 = ket_qua[2]
            ket_qua_04 = ket_qua[3]
            ket_qua_05 = ket_qua[4]
            ket_qua_06 = ket_qua[5]

            tesla_data = {
                'ky_quay_so': ky_quay_so,
                'ky_quay_ngay': ky_quay_ngay,
                'ky_quay_day': ky_quay_ngay[0:2],
                'ky_quay_month': ky_quay_ngay[3:5],
                'ky_quay_year': ky_quay_ngay[6:],
                'ket_qua_01': ket_qua_01,
                'ket_qua_02': ket_qua_02,
                'ket_qua_03': ket_qua_03,
                'ket_qua_04': ket_qua_04,
                'ket_qua_05': ket_qua_05,
                'ket_qua_06': ket_qua_06
            }

            yield tesla_data
