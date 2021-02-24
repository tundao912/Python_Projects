import scrapy

class TruecarSpider(scrapy.Spider):
    name="truecar"
    def start_requests(self):
        urls = ['https://www.truecar.com/used-cars-for-sale/listings/tesla/model-3/']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        all_listings = response.xpath('//div[@data-qa="Listings"]')
        for tesla in all_listings:
            make_model = tesla.css('div[data-test="vehicleListingCardTitle"] > div')
            year = make_model.css('span.vehicle-card-year::text').get()
            model_raw = make_model.css('span.vehicle-header-make-model').get()
            model = model_raw[model_raw.find('>') +1:-7].replace('<!-- -->', '')

            tesla_data = {
                'url': 'https://www.truecar.com' + tesla.css('a::attr(href)').get(),
                'model': year + ' ' + model,
                'mileage': tesla.css('div[data-test="vehicleMileage"]::text').get() + ' miles',
                'price': tesla.css('h4::text').get()

            }

            yield tesla_data