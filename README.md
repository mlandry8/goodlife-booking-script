# goodlife-booking-script

Quick & dirty script to help you book goodlife gym sessions before they fill up!

This script currently assumes you only have one gym favourited

**Prerequisites**

1. Chrome Webdriver: https://chromedriver.chromium.org/getting-started
2. Python3 (tested with python3.8)

**Setup**

1. Run `cp .env.example .env`
2. Fill in variables in newly created `.env` file with goodlife email and password

With runner shell script.

3. Run `./runner.sh`
4. If everything works, remove `--dry` arg in `runner.sh`

Alternativley, setup your venv and use the script manually.

4. `python booking_cript.py --headless --time-slot "6:00PM - 7:00PM" --days 7`

**Args**

```
--dry                 run a dry-run - everything except for booking
--headless            run in headless browser mode
--time-slot           desired time-slot. str format ex: "6:00PM - 7:00PM"
--days                how many days in the future to book
```


Note: you probably need to modify the runner slightly if you want to execute from a cronjob
