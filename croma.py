from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import openpyxl
import time
import pandas as pd

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    
    service = Service()  # Update path if needed
    driver = webdriver.Chrome()  # ✅ Fix: Properly pass service and options
    return driver

def main(search_item, max_clicks=1):
    driver = setup_driver()
    try:
        url = f"https://www.croma.com/searchB?q={search_item}%3Arelevance&text={search_item}"
        driver.get(url)

        products = []
        
        for _ in range(max_clicks):
            try:
                load_more_button = driver.find_element(By.XPATH, "//button[contains(text(),'View More')]")
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)  # Wait for new data to load
            except:
                break  # Stop if button not found

        product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-item")

        for item in product_elements:
            time.sleep(0.5)
            try:
                name = item.find_element(By.CSS_SELECTOR, ".product-title").text
            except:
                name = "N/A"
            
            try:
                price = item.find_element(By.CSS_SELECTOR, ".amount").text
                price = price.replace(".", "").replace("₹", "").replace(",","")
            except:
                price = "N/A"
            
            try:
                rating = item.find_element(By.CSS_SELECTOR, ".rating-text").text
            except:
                rating = "N/A"
            
            try:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                link = "N/A"
            
            try:
                image = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")  # ✅ Fetch Image
            except:
                image = "N/A"
            
            products.append({
                "Name": name,
                "Price": price,
                # "Rating": rating,
                "Link": link,
                "Image": image
            })

        # return products  # ✅ Ensure function returns data
        save_to_excel(products,f"{search_item}_croma.xlsx")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()  # ✅ Ensure the browser is closed in all cases

def save_to_excel(products, filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Croma Products"

    headers = ["Name", "Price", "Link", "Image"]
    sheet.append(headers)

    for product in products:
        sheet.append([
            product["Name"], 
            product["Price"], 
            # product["Rating"], 
            product["Link"],
            product["Image"] 
        ])

    workbook.save(filename)
    print(f"Data saved to {filename}")
    save_to_csv(filename)
    
def save_to_csv(filename):
    f = filename[:-5:1]
    df = pd.read_excel(filename)
    df = df.dropna()
    df.to_csv(f+'.csv',index=False)

# if __name__ == "__main__":
#     search_item = input("Enter item to search: ").strip()
#     products = main(search_item)

#     if products:
#         save_to_excel(products, f"{search_item}_croma.xlsx")
#         print(f"Scraping completed! Data saved to '{search_item}_croma.xlsx'")
#     else:
#         print("No data scraped.")
