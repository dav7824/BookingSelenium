#!/usr/bin/env python
# -*- coding: utf-8 -*-
import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport

from selenium import webdriver
from selenium.webdriver.common.by import By
from prettytable import PrettyTable
import os
import time


class Booking(webdriver.Chrome):
    def __init__(self, driver_path, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path  # add driver to system path
        super(Booking, self).__init__()
        self.implicitly_wait(5)  # waiting time for each processing
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)
        try:
            # close the pop-up if appears
            close_ad = self.find_element(By.CSS_SELECTOR,
            'button[aria-label="關閉登入的資訊。"]')
            close_ad.click()
        except:
            print('No ad shown, continue...')

    # execute before ending context manager
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def change_currency(self, currency='USD'):
        currency_element = self.find_element(By.CSS_SELECTOR,
                'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()
        selected_currency_element = self.find_element(By.XPATH,
                f'//button//div[contains(text(),"{currency}")]/..')
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        # get search box
        search_field = self.find_element(By.CSS_SELECTOR,
                'input[placeholder="你要去哪裡？"]')
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(2)  # wait for autocompletion
        # get whole list of autocompletion
        auto_comp = self.find_element(By.CSS_SELECTOR,
                'ul[data-testid="autocomplete-results"]')
        # get list of autocompletion results
        auto_comp_results = auto_comp.find_elements(By.XPATH,
                '//li[.//div[@data-testid="autocomplete-result"]]')
        # click 1st autocompletion result
        auto_comp_results[0].click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.XPATH,
                f'//td[.//span[@data-date="{check_in_date}"]]')
        check_in_element.click()
        check_out_element = self.find_element(By.XPATH,
                f'//td[.//span[@data-date="{check_out_date}"]]')
        check_out_element.click()

    def select_adults(self, adult_count):
        # open the count selection menu
        self.find_element(By.CSS_SELECTOR,
                'button[data-testid="occupancy-config"]').click()
        # find the div of adult count functionality
        adult_div = self.find_element(By.XPATH,
                '//div/div/label[@for="group_adults"]/../..')
        # find the default adult count
        adult_count_default = int( adult_div.find_element(By.XPATH,
                '//span[number(.)=.]').get_attribute('innerHTML') )
        # calcuate the change to be applied to adult count
        adult_count_delta = adult_count - adult_count_default
        # find adult count change buttons
        adult_buttons = adult_div.find_elements(By.CSS_SELECTOR,
                'button[type="button"]')
        adult_button_dec = adult_buttons[0]  # button for decreasing
        adult_button_inc = adult_buttons[1]  # button for increasing
        # change adult count to desired value
        if adult_count_delta >= 0:
            adult_button = adult_button_inc
        else:
            adult_button = adult_button_dec
        for _ in range(abs(adult_count_delta)):
            adult_button.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR,
                'button[type="submit"]')
        search_button.click()

    def apply_filtration(self, *star_values):
        filtration = BookingFiltration(self)
        filtration.apply_star_rating(*star_values)
        time.sleep(5)  # wait for star filtration to complete
        filtration.sort_price_lowest_first()

    def report_result(self):
        self.refresh()  # to let bot grab data properly
        hotel_boxes = self.find_element(By.ID, 'search_results_table')
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
                field_names = ['Hotel Name', 'Hotel Price']
                )
        table.add_rows( report.pull_deal_box_attributes() )
        print(table)
