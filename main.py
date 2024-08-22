from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta

import os
import time
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np

#
#
# adjust y-axis (price) scaling
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
            # print("hours" + now - timedelta(hours=hours))
            return now - timedelta(hours=hours)
            
        elif "minutes" in date_str:
            minutes = int(date_str.split()[0])
            # print("minutes" + now - timedelta(minutes=minutes))
            return now - timedelta(minutes=minutes)
    else:
        # print(datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S"))
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")

files_exist = input("Do you have the price and date txt files already (y/n): ")

while files_exist != 'y' and files_exist != 'n':
    files_exist = input("Please enter either y for yes or n for no:")

if files_exist == "n":
    url = input("Please enter the entire URL for the collection you would like to chart: ")
    driver = webdriver.Chrome(service=Service("chromedriver.exe"))
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

    print("Gathering data, please wait...")

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
    all_dates.reverse()

    with open("prices.txt", "w") as file:
        for number in all_prices:
            file.write(f"{number}\n")

    with open("dates.txt", "w") as file:
        for number in all_dates:
            file.write(f"{number}\n")

print("\n\nCreating Chart...\n")

with open('prices.txt', 'r') as file:
    prices = [float(line.strip()) for line in file.readlines()]

with open("dates.txt", "r") as file:
    dates = [line.strip() for line in file.readlines()]


all_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

# Uncomment if text file contains prices from newest to oldest
# prices.reverse()

# Create an interactive line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=all_dates,
    y=prices,
    mode='lines',
    name='Price',
    line=dict(color='blue')
))

# Update layout to include range slider and selectors
fig.update_layout(
    title="Price Trend",
    xaxis_title="Date",
    yaxis_title="Price (DOGE)",
    xaxis=dict(
        rangeslider=dict(visible=True),  # Adds a range slider for the x-axis
        type="date"
    ),
    height=600,
    width=1400
)

fig.show()

# plt.figure(figsize=(40, 6))

# # Plot prices
# plt.plot(all_dates, all_prices, marker='o', linestyle='-', color='b')
# plt.title("Price Trend")
# plt.xlabel("Date")
# plt.ylabel("Price (DOGE)")
# plt.grid(True)

# # Display every 200 ticks
# min_price = min(all_prices)
# max_price = max(all_prices)
# num_ticks = float(max_price)/500;
# # yticks(np.arange(num_ticks,200,1))
# # plt.yticks(yticks)

# # Format for better readability
# plt.gcf().autofmt_xdate()
# plt.show()




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