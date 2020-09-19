import os
import argparse
import logging

from time import sleep
from datetime import datetime, timedelta

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)

load_dotenv()
USERNAME = os.getenv('GOODLIFE_USERNAME')
PASSWORD = os.getenv('GOODLIFE_PASSWORD')

if not USERNAME or not PASSWORD:
    logging.error('username/password not defined in .env file')
    exit(1)

def wait_for_element_by(browser, element_name, element_type):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((element_type, element_name)))
        sleep(2)
    except TimeoutException:
        print ("Loading took too much time!")


def book_gym_session(browser, day, time, dry_run=False):
    # navigate to login page (will redirect to bookings page)
    browser.get('https://www.goodlifefitness.com/members/bookings/workout')

    # login
    logging.info(f'Logging in with username {USERNAME}')
    browser.find_element_by_name('Email/Member #').send_keys(USERNAME)
    browser.find_element_by_name('Password').send_keys(PASSWORD)

    wait_for_element_by(browser, 'btn-login', By.ID)
    browser.find_element_by_id('btn-login').click()

    # select date x days from now
    week_from_now = datetime.now() + timedelta(days=day)
    week_from_now = week_from_now.strftime('%Y-%m-%d')

    logging.info(f'Selecting date {week_from_now}')
    wait_for_element_by(browser, 'date-tile', By.CLASS_NAME)
    [
        elem for elem in browser.find_elements_by_class_name('date-tile')
        if elem.get_attribute('data-date') == week_from_now
    ][0].click()


    # select appropriate timeframe to book
    logging.info(f'Selecting session time {time}')
    wait_for_element_by(browser, 'cmp-button', By.CLASS_NAME)
    try:
        book_time = [
            elem for elem in browser.find_elements_by_class_name('cmp-button')
            if elem.get_attribute('data-display') == time and not elem.get_attribute('disabled')
        ][0].click()
    except IndexError as e:
        logging.error(f'Time {time} is fully booked')
        return False

    # accept code of conduct
    logging.info(f'Agreeing to terms')
    wait_for_element_by(browser, 'codeOfConductAgree', By.ID)
    browser.find_element_by_id('codeOfConductAgree').click()

    # confirm and book session
    if not dry_run:
        sleep(1)
        browser.find_element_by_id('confirmBookingButton').click()
    else:
        logging.info('** DRY RUN **')
    logging.info('Booking confirmed')

    return True


if __name__ == '__main__':
    # setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dry', action='store_true',
        help='run a dry-run - everything except for booking'
    )
    parser.add_argument(
        '--headless', action='store_true',
        help='run in headless browser mode'
    )
    parser.add_argument(
        '--time-slot', type=str, default='6:00PM - 7:00PM',
        help='desired time-slot. str format ex: "6:00PM - 7:00PM"'
    )
    parser.add_argument(
        '--days', type=int, default=7,
        help='how many days in the future to book'
    )
    args = parser.parse_args()

    # setup browser with chrome webdriver 
    options = Options()
    options.headless = args.headless
    browser = webdriver.Chrome(options=options)

    # book session
    success = book_gym_session(browser, args.days, args.time_slot, args.dry)

    # close browser & exit
    browser.close()
    browser.quit()

    logging.info('Exiting')
    exit(int(not success))
