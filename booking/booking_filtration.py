#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.CSS_SELECTOR,
                'div[data-filters-group="class"')
        for val in star_values:
            star_check = star_filtration_box.find_element(By.XPATH,
                    f'//div[contains(text(),"{val} 星級")]')
            star_check.click()

    def sort_price_lowest_first(self):
        sort_button = self.driver.find_element(By.CSS_SELECTOR,
                'button[data-testid="sorters-dropdown-trigger"]')
        sort_button.click()
        self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]').click()
