from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import time
import requests
import pandas as pd

def setup_driver():
    """Set up Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_vijay_sales(search_query, num_pages=1):
    """Scrape product data from Vijay Sales."""
    time.sleep(5)
    driver = setup_driver()
    products = []

    for page in range(1, num_pages + 1):
        url = f"https://www.vijaysales.com/search-listing?q={search_query}&page={page}"
        print(f"🔍 Scraping Page {page}: {url}")
        
        # Request page to verify connection
        requests.get(url, verify=False)
        driver.get(url)

        # Wait until products are loaded
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
        except:
            print("❌ No products found on this page.")
            continue  # Skip to next page

        time.sleep(3)  # Allow time for page load
        items = driver.find_elements(By.CSS_SELECTOR, ".product-card")

        for item in items:
            try:
                name = item.find_element(By.CSS_SELECTOR, ".product-name").text.strip()
            except:
                name = "N/A"

            try:
                price = item.find_element(By.CSS_SELECTOR, ".discountedPrice").get_attribute("data-price")
                price = price.replace(",","")
                price = int(price)
            except:
                price = "N/A"

            try:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                link = "N/A"

            try:
                image = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            except:
                image = "N/A"

            products.append({"Name": name, "Price": price, "Link": link, "Image": image})

    driver.quit()
    return products

def save_to_excel(products, filename):
    """Save scraped data to an Excel file."""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Vijay Sales Products"

    headers = ["Name", "Price", "Link", "Image"]
    sheet.append(headers)

    for product in products:
        sheet.append([product["Name"], product["Price"], product["Link"], product["Image"]])

    workbook.save(filename)
    print(f"✅ Data saved to {filename}")
    save_to_csv(filename)

def save_to_csv(filename):
    """Convert Excel file to CSV."""
    csv_filename = filename.replace(".xlsx", ".csv")
    df = pd.read_excel(filename)
    df = df.dropna()
    df.to_csv(csv_filename, index=False)
    print(f"✅ Data also saved to {csv_filename}")

def main(search_term):
    """Main function to scrape and save data."""
    products = scrape_vijay_sales(search_term)

    if products:
        file_name = f"{search_term}_vijay.xlsx"
        save_to_excel(products, file_name)
        print(f"🎉 Scraping completed! Check '{file_name}' and its CSV version.")
    else:
        print("❌ No data found.")

# Run script for a test case (you can replace 'laptop' with any product)

# Uncomment below for user input version:
# if __name__ == "__main__":
#     search_item = input("Enter product to search: ")
#     main(search_item)
