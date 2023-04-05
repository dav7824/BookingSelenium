#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR,
                'div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(By.CSS_SELECTOR,
                    'div[data-testid="title"]').get_attribute('innerHTML')
            hotel_price = deal_box.find_element(By.CSS_SELECTOR,
                    'span[data-testid="price-and-discounted-price"]').get_attribute('innerHTML')
            '''hotel_score = deal_box.find_element(By.XPATH,
                    '//div[contains(@aria-label, "分數")]').get_attribute('innerHTML')'''
            collection.append( [hotel_name, hotel_price] )
        return collection
