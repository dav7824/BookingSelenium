#!/usr/bin/env python
from booking.booking import Booking
import time

with Booking() as bot:
    bot.land_first_page()
    #bot.change_currency('GBP')
    bot.select_place_to_go('New York')
    bot.select_dates('2023-04-08', '2023-05-12')
    bot.select_adults(4)
    #bot.select_adults(1)
    bot.click_search()
    bot.apply_filtration(3, 4)
    bot.report_result()
    time.sleep(30)
