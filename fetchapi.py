import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import csv

# Define base directory and driver paths
BASE_DIR = os.path.dirname(os.curdir)
DRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver-win64', 'chromedriver.exe')
CHROME_PATH = os.path.join(BASE_DIR, 'chrome-win64', 'chrome.exe')
LIMIT_ITEMS = 500

def fetch_categories(driver):
    """Fetch the product categories from the catalog API."""
    url = "https://www.lacolonia.com.ni/api/Catalog/AllCategories/LACOLONIA/es"
    
    # Retrieve cookies
    cookies = driver.get_cookies()
    
    # Prepare headers
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Language": "es",
    }

    # Add cookies to the request
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    try:
        # Make the GET request to fetch categories
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Parse the JSON response
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return None

def fetch_api_data(category, driver):
    url = f"https://www.lacolonia.com.ni/api/BranchOfficeProduct/CarouselByCategories/LACOLONIA/c6otGqNhcP/es/{category}/false/false"
    
    # Retrieve cookies
    cookies = driver.get_cookies()
    
    # Prepare headers
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Language": "es",
    }

    # Add cookies to the request
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    try:
        # Make the GET request to the API
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Parse the JSON response
    except Exception as e:
        print(f"Error fetching data for category '{category}': {e}")
        return None

def save_csv(products):
    # Save the results to a CSV file
    with open('productsapi.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Product Code', 'Business ID', 'Brand', 'Product Name', 'Product Description', 'Model',
                         'Color', 'Price', 'In Stock', 'Quantity', 'Collect Tax', 'Creation Date',
                         'Active', 'Tags', 'Views Count', 'Show In Featured', 'With Discount', 
                         'Discount Value', 'Image Alternative Text', 'Resource Link', 
                         'Product Type', 'Products Sold', 'Is Wish'])
        
        for product in products:
            # Write the data
            writer.writerow([
                product.get("ProductCode"),
                product.get("BusinessId"),
                product.get("Brand"),
                product.get("ProductName"),
                product.get("ProductDescription"),
                product.get("Model"),
                product.get("Color"),
                product.get("Price"),
                product.get("InStock"),
                product.get("Quantity"),
                product.get("CollectTax"),
                product.get("CreationDate"),
                product.get("Active"),
                product.get("Tags"),
                product.get("ViewsCount"),
                product.get("ShowInFeatured"),
                product.get("WithDiscount"),
                product.get("DiscountValue"),
                product.get("ImageAlternativeText"),
                product.get("ResourceLink"),
                product.get("ProductType"),
                product.get("ProductsSold"),
                product.get("IsWish")
            ])

    print("Data saved to productsapi.csv")

def main():
    # Initialize the Chrome WebDriver with options
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
    driver = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)

    try:
        print("Navigating to La Colonia...")
        # Navigate to the main page to set cookies
        driver.get("https://www.lacolonia.com.ni")
        time.sleep(3)  # Wait for the page to load, adjust if necessary

        # Fetch categories
        categories_data = fetch_categories(driver)
        categories = [cat["CategoryCode"] + f":{LIMIT_ITEMS}" for cat in categories_data]  # Modify as needed

        all_products = []  # List to hold all products

        # Iterate through categories and fetch data
        for category in categories:
            print(f"Fetching products for category: {category}...")
            data = fetch_api_data(category, driver)
            
            if data:
                print(f"Products for {category}:")
                for key, products in data.items():
                    all_products.extend(products)  # Add products to the all_products list

        # Save all products to CSV
        if all_products:
            save_csv(all_products)

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
