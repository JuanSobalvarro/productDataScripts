from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import csv

# Define base directory and driver paths
BASE_DIR = os.path.dirname(os.curdir)
DRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver-win64', 'chromedriver.exe')
CHROME_PATH = os.path.join(BASE_DIR, 'chrome-win64', 'chrome.exe')

def cleanList(list: list[str]) -> list[str]:
    newList: list[str] = []
    for item in list:
        item_name = item.text.strip()
        if item_name != '':
            newList.append(item_name)
    return newList  

def main():
    # Configure web driver
    chrome_options = Options()
    chrome_options.binary_location = CHROME_PATH
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    service = Service(DRIVER_PATH)

    # Initialize web driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the webpage
        url = "https://www.lacolonia.com.ni"  # Replace with the actual URL
        driver.get(url)

        # Wait for the page to load fully
        time.sleep(5)

        # Scroll until the bottom of the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(1)

            # Calculate new scroll height and compare with the last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # If heights are the same, the page is fully scrolled
            last_height = new_height

        # Now, scrape product names and prices
        products_raw = driver.find_elements(By.CLASS_NAME, 'item-caption')
        price_elements = driver.find_elements(By.CLASS_NAME, 'item-price')

        products = cleanList(products_raw)
        prices = cleanList(price_elements)

        # Clean discounts
        for price in prices:
            if price.find('%') != -1:
                prices.remove(price)

        # Collect all the data in a list
        product_price_list = []

        if len(products) == len(prices):
            print("Logic is good uwunya")

        for product, price in zip(products, prices):
            product_price_list.append((product, price))


        # Save the results to a CSV file
        with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Regular Price', 'Discounted Price'])  # Write the header
            for item in product_price_list:
                writer.writerow(item)  # Write the data

        print("Data saved to products.csv")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
