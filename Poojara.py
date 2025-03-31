import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def scrape_poojaratele(search_term):
    print("hi")
    search_url = f"https://www.poojaratele.com/catalogsearch/result/?q={search_term}"  # Example category URL
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return []

    # soup = BeautifulSoup(response.text, 'html.parser')

    soup = BeautifulSoup(response.text, 'html.parser')

    s=(soup.prettify())  # Print full HTML to check structure
    html_content = s

    soup = BeautifulSoup(html_content, "html.parser")
    products = []
    

    # Find all product containers; adjust the selector based on the website's structure
    for item in soup.find_all("li", class_="item product product-item"):
        try:
            print("hello deep")
            name_tag = item.find("a", class_="product-item-link")
            price_tag = item.find("span", class_="price")
            image_tag = item.find("img", class_="product-image-photo main-img")
            product_url = name_tag["href"] if name_tag else None

            product = {
                "Name": name_tag.text.strip() if name_tag else None,
                "Price": price_tag.text.strip() if price_tag else "Price Not Available",
                "Link": product_url,
                "Image": image_tag["src"] if image_tag else None,
            }

            products.append(product)
        except:
            print()

    save_to_csv(products,search_term)


def save_to_csv(data,search_term):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(search_term+'_poojara.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    print(f"Data saved to {search_term}")

# search_url = f"https://www.poojaratele.com/catalogsearch/result/?q={}"  # Example category URL
# product_data = scrape_poojaratele(search_url)

# if product_data:
#     save_to_csv(product_data)
#     print("Data scraped successfully")
# else:
#     print("No data scraped.")
# scrape_poojaratele("Laptop")