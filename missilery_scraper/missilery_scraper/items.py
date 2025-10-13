"""
Scrapy items for the Missilery scraper project.

This module defines the data structures used to store scraped missile data
in a structured format for processing and storage.
"""

import scrapy


class IndexPageItem(scrapy.Item):
    """Item for storing index page data"""
    url = scrapy.Field()
    page_number = scrapy.Field()
    html_content = scrapy.Field()
    missile_links = scrapy.Field()

class DetailPageItem(scrapy.Item):
    """Item for storing detail page data"""
    url = scrapy.Field()
    missile_name = scrapy.Field()
    html_content = scrapy.Field()

class MissileItem(scrapy.Item):
    """Item for storing structured missile data"""
    missile = scrapy.Field()
    name = scrapy.Field()
    purpose = scrapy.Field()
    base = scrapy.Field()
    warhead = scrapy.Field()
    guidance_system = scrapy.Field()
    country = scrapy.Field()
    range_km = scrapy.Field()
    year_developed = scrapy.Field()
    description = scrapy.Field()
    index_page_url = scrapy.Field()
    detail_page_url = scrapy.Field()
    page_number = scrapy.Field()
    technical_characteristics = scrapy.Field()

    # Detailed information fields
    is_detailed = scrapy.Field()
    range_detailed = scrapy.Field()
    speed = scrapy.Field()
    weight = scrapy.Field()
    length = scrapy.Field()
    diameter = scrapy.Field()
    wingspan = scrapy.Field()
    height = scrapy.Field()
    accuracy = scrapy.Field()
    flight_time = scrapy.Field()
    flight_altitude = scrapy.Field()
    engine_type = scrapy.Field()
    thrust = scrapy.Field()
    burn_time = scrapy.Field()
    fuel_type = scrapy.Field()
    guidance_system_detailed = scrapy.Field()
    warhead_detailed = scrapy.Field()
    fuse_type = scrapy.Field()
    country_detailed = scrapy.Field()
    developer = scrapy.Field()
    manufacturer = scrapy.Field()
    year_developed_detailed = scrapy.Field()
    adoption_year = scrapy.Field()
    status = scrapy.Field()
    quantity = scrapy.Field()
    other_characteristics = scrapy.Field()
    images = scrapy.Field()

    # New structured content fields
    structured_content = scrapy.Field()
    characteristics_table = scrapy.Field()
    image_urls = scrapy.Field()
    gallery_images = scrapy.Field()
    detailed_filename = scrapy.Field()
    scraped_at = scrapy.Field()
