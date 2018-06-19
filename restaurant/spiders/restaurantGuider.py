# -*- coding: utf-8 -*-
import scrapy


class RestaurantguiderSpider(scrapy.Spider):
    name = 'restaurantGuider'
    start_urls = ['https://www.tripadvisor.com/Restaurants-g293962-Colombo_Western_Province.html']


    def restaurantDetail(self, response):
        name = response.css('h1.heading_title::text').extract_first()
        street_address = response.css('span.street-address::text').extract_first()
        extended_address = response.css('span.extended-address::text').extract_first()
        locality = response.css('span.locality::text').extract_first()
        days=response.css('span.day::text').extract()
        hours=response.css('div.hoursRange::text').extract()
        phone=response.css('div.blEntry.phone span::text').extract_first()
        rating=response.css('span.overallRating::text').extract()[0]
        cuisines=response.css('div.text::text').extract()[-1]
        tags=response.css('div.keywords a::attr(data-keyword)').extract()
        goodFor=response.css('div.table_section div.row div.content::text').extract()[6][1:-1]
        meals=response.css('div.table_section div.row div.content::text').extract()[4][1:-1]
        features=response.css('div.table_section div.row div.content::text').extract()[5][1:-1]
        description=response.css('div.details_tab div.content::text').extract()[-1][1:-1]
        nearby=response.css('div.poiName::text').extract()

        yield {
            'place_name':name ,
            'street_address':street_address ,
            'extended_address':extended_address ,
            'locality': locality,
            'phone':phone,
            'rating': rating ,
            'cuisines':cuisines,
            'tags':tags,
            'open_hours': hours,
            'open_days':days,
            'good_for':goodFor,
            'meals':meals,
            'features':features,
            'description':description,
            'nearby': nearby,
        }

    def parse(self, response):

        for hotel in response.css('a.property_title'):
            yield response.follow(hotel, self.restaurantDetail)

        a = response.css('a.next::attr(href)').extract_first()
        if (a != None):
            yield response.follow('https://www.tripadvisor.com' + a, self.parse)


