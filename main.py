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
driver = webdriver.Chrome(service=Service("chromedriver.exe"))

# Change the url to the specific collection
url = 'https://doggy.market/nfts/minidoges'
driver.get(url)

all_prices = []

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
    except (RuntimeError, TypeError, NameError):
        print("Timeout occurred, element not found.")
        break
    
    # Append all found prices
    for element in price_elements:
        if element.text == "Price":
            continue
        all_prices.append(element.text)
        print(element.text)

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

with open("miniDogesPriceHistory.txt", "w") as file:
    for number in all_prices:
        file.write(f"{number}\n")

plt.figure(figsize=(40, 6))

# Plot prices
plt.plot(all_prices, marker='o', linestyle='-', color='b')
plt.title("Price Trend of Mini Doges")
plt.xlabel("Data Points (Starting from the Latest)")
plt.ylabel("Price (USD)")
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