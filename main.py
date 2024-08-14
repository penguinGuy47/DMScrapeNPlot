from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta

import requests
import time
import matplotlib.pyplot as plt

#
#
# grab the dates and parse
#
#


# Setup Selenium
# options = Options()
# options.headless = True  # Run in headless mode
# driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

def parse_date(date_str):
    if "ago" in date_str:
        now = datetime.now()
        if "hours" in date_str:
            hours = int(date_str.split()[0])
            print(now - timedelta(hours=hours))
            return now - timedelta(hours=hours)
            
        elif "minutes" in date_str:
            minutes = int(date_str.split()[0])
            print(now - timedelta(minutes=minutes))
            return now - timedelta(minutes=minutes)
    else:
        print(datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S"))
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    
driver = webdriver.Chrome(service=Service("chromedriver.exe"))

# Change the url to the specific collection
url = 'https://doggy.market/nfts/doginaldogs'
driver.get(url)

all_prices = []
all_dates = []

time.sleep(4)
wait = WebDriverWait(driver, 10)
tabs_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabs-wrapper")))

# Locate and click the "Activity" tab
activity_tab = driver.find_element(By.XPATH, "//li[contains(text(), 'Activity')]")
activity_tab.click()
time.sleep(4)

while True:
    wait = WebDriverWait(driver, 20) 
    try:
        # price_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "usd-value")))
        price_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "price")))
        date_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "date")))
    except (RuntimeError, TypeError, NameError):
        print("Timeout occurred, element not found.")
        break
    
    # add prices to array
    for element in price_elements:
        if element.text == "Price":
            continue
        price_text = element.text.replace(',', '')
        all_prices.append(price_text)
        # print(price_text)

    # add dates to array
    for dt in date_elements:
        # skip elements that just contains "Date"
        if dt.text == "Date":
            continue
        else:
            print("appending")
            all_dates.append(parse_date(dt.text))
            
        # date_text = dt.text.replace()

    # Check the "Next" button's aria-disabled attribute
    next_button = driver.find_element(By.XPATH, "//li[@class='pagination-item next']")
    is_disabled = next_button.get_attribute("aria-disabled")

    if is_disabled == "true":
        print("No more pages to load.")
        break
    else:
        # Click the "Next" button to move to the next page
        next_button.click()
        time.sleep(1)

driver.quit()

all_prices.reverse()

with open("output.txt", "w") as file:
    for number in all_prices:
        file.write(f"{number}\n")

plt.figure(figsize=(40, 6))

# Plot prices
plt.plot(all_prices, marker='o', linestyle='-', color='b')
plt.title("Price Trend")
plt.xlabel("Data Points (Starting from the Latest)")
plt.ylabel("Price (DOGE)")
plt.grid(True)
plt.show()




    # FOR LISTED PRICES
    # price_element = driver.find_elements(By.CLASS_NAME, "usd-value")

    # for element in price_element:
    #     all_prices.append(element.text)

    # next_button = driver.find_element(By.XPATH, "//li[@class='pagination-item next']")
    # is_disabled = next_button.get_attribute("aria-disabled")

    # if is_disabled == "true":
    #     print("No more pages to load.")
    #     break
    # else:
    #     next_button.click()
    #     time.sleep(6)