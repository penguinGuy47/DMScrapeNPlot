from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import matplotlib.pyplot as plt

# Setup Selenium with optimized options
options = Options()
options.add_argument("--headless")  # Ensure headless mode is enabled
options.add_argument("--disable-gpu")  # Disable GPU for faster performance
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection as a bot
options.add_argument("--disable-images")  # Disable loading images
options.add_argument("--disable-extensions")  # Disable browser extensions
options.add_argument("--disable-infobars")  # Disable infobars
options.add_argument("--disable-javascript")  # Disable JavaScript if not needed

# Provide the path to your ChromeDriver executable
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# Get the dynamic content
url = 'https://doggy.market/nfts/minidoges'
driver.get(url)

all_prices = []

# Use WebDriverWait instead of time.sleep for better performance
wait = WebDriverWait(driver, 10)
tabs_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabs-wrapper")))

# Locate and click the "Activity" tab
activity_tab = driver.find_element(By.XPATH, "//li[contains(text(), 'Activity')]")
activity_tab.click()

while True:
    try:
        price_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "price")))
    except Exception as e:
        print(f"Timeout occurred: {e}")
        break
    
    # Append all found prices to the list
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
        time.sleep(1)  # Reduced time.sleep to make it faster

driver.quit()

all_prices.reverse()

with open("miniDogePriceHistory.txt", "w") as file:
    # Loop through each integer in the array
    for number in all_prices:
        # Write each integer to the file followed by a newline character
        file.write(f"{number}\n")

# Increase plot size
plt.figure(figsize=(40, 6))

# Plotting the prices on a line chart
plt.plot(all_prices, marker='o', linestyle='-', color='b')
plt.title("Price Trend of Mini Doges")
plt.xlabel("Data Points (Starting from the Latest)")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.show()
