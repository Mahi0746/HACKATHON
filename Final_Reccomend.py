import pandas as pd
import webbrowser

import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import webbrowser

def search(search_term):
    # Load the Excel files with source names
    search_croma = search_term.strip()+"_croma.xlsx"
    search_vijay = search_term.strip()+"_vijay.xlsx"
    search_poojara = search_term.strip()+"_poojara.csv"
    files = {search_croma: "Croma",search_vijay:"Vijay",search_poojara:"Poojara"}
    
    df_list = []
    for file, source in files.items():
        if source == "Poojara":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        df["Website"] = source  # Add a website column
        df_list.append(df)
    
    # Combine all DataFrames
    df = pd.concat(df_list, ignore_index=True)
    
    # Ensure the 'Link' column exists in the DataFrame
    if "Link" not in df.columns:
        print("Error: 'Link' column not found in the Excel file.")
        return None
    
    filtered_search = df[df["Name"].str.contains(search_term, case=False, na=False)].copy()  # Explicit copy

    # Remove any non-numeric characters (like ₹, $, commas) and convert to numeric
    filtered_search.loc[:, "Price"] = (
        filtered_search["Price"]
        .astype(str)                      
        .str.replace("₹", "")  
        .str.replace(",", "")
        .str.replace(".", "")
        .astype(float)                    # Convert to float
    )

    filtered_search = filtered_search.dropna(subset=["Price"])  # Remove rows with NaN prices
    sorted_search = filtered_search.sort_values(by=["Price"], ascending=True).reset_index(drop=True)

    if sorted_search.empty:
        print("No search found matching your search.")
        return None

    print(sorted_search[["Price" , "Name", "Website", "Link","Image"]])

    # Ask user if they want to see a graph
    visualize_data(sorted_search, search_term)

    # Feature: Allow user to open a product page
    # open_product_page(sorted_search)

    # return sorted_search  # Return DataFrame for further processing if needed

def visualize_data(df, search_term):
    # while True:
        # print("\nWould you like to visualize the data?")
        # print("1. Price Comparison (Bar Chart)")
        # print("2. Website Distribution (Pie Chart)")
        # print("3. Price vs Rating (Scatter Plot)")
        # print("4. Price Distribution (Histogram)")
        # print("5. Exit")

        # choice = input("Enter your choice: ")

        # if choice == "1":
        compare_avg_price_by_website(df)
        # elif choice == "2":
        view_price_distribution(df, search_term)
        # elif choice == "3":
            # view_price_vs_rating(df, search_term)
        # elif choice == "4":
        view_price_histogram(df, search_term)
        # else:
        #     break




def compare_avg_price_by_website(df):
    # Group by 'Website' and calculate average price
    avg_price = df.groupby("Website")["Price"].mean()

    # Plot Bar Chart
    plt.figure(figsize=(8, 5))
    avg_price.plot(kind="bar", color=["blue", "red", "green", "orange"])

    plt.xlabel("Website", fontsize=12)
    plt.ylabel("Average Price (₹)", fontsize=12)
    plt.title("Average Price Comparison by Website", fontsize=14)
    plt.savefig('./static/charts/price.png')
    plt.clf()
    # Show price labels on top of bars
    for index, value in enumerate(avg_price):
        plt.text(index, value + 1000, f"₹{int(value)}", ha='center', fontsize=10, color="black")

    plt.xticks(rotation=0)  # Keep website names horizontal
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # plt.show()

def view_price_distribution(df, search_term):  # Pie Chart
    website_counts = df["Website"].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(website_counts, labels=website_counts.index, autopct="%1.1f%%", colors=["blue", "red","green"])
    plt.title(f"Product Distribution for {search_term}")
    plt.savefig('./static/charts/price_dist.png')
    plt.clf()

    # plt.show()

# def view_price_vs_rating(df, search_term):
#     if "Rating" not in df.columns:
#         print("No rating data available.")
#         return

#     # df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")  # Convert to numbers
#     df = df.dropna(subset=["Price", "Rating"])  # Drop missing values

#     print(f"Number of valid data points: {len(df)}")  # Debugging

#     if df.empty:
#         print("No valid data available for visualization.")
#         return

#     plt.figure(figsize=(8, 5))
#     plt.scatter(df["Price"], df["Rating"], c='blue', alpha=0.6)
#     plt.xlabel("Price")
#     plt.ylabel("Rating")
#     plt.title(f"Price vs Rating for {search_term}")
#     plt.grid(True)
#     plt.show()



def view_price_histogram(df, search_term):  # Histogram
    plt.figure(figsize=(8, 5))
    plt.hist(df["Price"], bins=10, color='green', alpha=0.7)
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.title(f"Price Distribution for {search_term}")
    plt.grid(True)
    plt.savefig('./static/charts/histogram.png')
    plt.clf()


def open_product_page(df):
    try:
        number = int(input(f"\nEnter a number (0 to {len(df)-1}) to open the product page: "))
        if 0 <= number < len(df):
            product_url = df.iloc[number]["Link"]  # Use the correct 'Link' column
            if pd.notna(product_url):  # Check if URL exists
                print(f"Opening: {product_url}")
                webbrowser.open(product_url)
            else:
                print("No URL available for this product.")
        else:
            print("Invalid number. Please enter a valid index.")
    except ValueError:
        print("Invalid input. Please enter a number.")



# def search_Fridge(search_term):
#     # Load the Excel files with source names
#     files = {"fridge_croma.xlsx": "Croma", "fridge_ebay.xlsx": "Ebay"}
    
#     df_list = []
#     for file, source in files.items():
#         df = pd.read_excel(file)
#         df["Website"] = source  # Add a website column
#         df_list.append(df)
    
#     # Combine all DataFrames
#     df = pd.concat(df_list, ignore_index=True)
    
#     # Ensure the 'Link' column exists in the DataFrame
#     if "Link" not in df.columns:
#         print("Error: 'Link' column not found in the Excel file.")
#         return
    
#     # Filter the DataFrame based on the search term (case-insensitive)
#     filtered_fridge = df[df["Name"].str.contains(search_term, case=False, na=False)].copy()  # Explicit copy to avoid warnings
    
#     # Clean the 'Price' column (remove currency symbols and commas) and convert to float
#     filtered_fridge.loc[:, "Price"] = (
#         filtered_fridge["Price"]
#         .astype(str)                      # Ensure it's a string
#         .str.replace(r"[^\d.]", "", regex=True)  # Remove non-numeric characters except dots
#         .astype(float)                    # Convert to float
#     )

#     # Remove rows where price conversion failed
#     filtered_fridge = filtered_fridge.dropna(subset=["Price"])

#     # Sort the filtered results by Price (ascending)
#     sorted_fridge = filtered_fridge.sort_values(by=["Price"], ascending=True).reset_index(drop=True)
    
#     # Display results
#     if sorted_fridge.empty:
#         print("No fridges found matching your search.")
#         return
    
#     print(sorted_fridge[["Price", "Name", "Website", "Link"]])  # Display links in output

#     visualize_data(sorted_fridge, search_term)
    
#     try:
#         number = int(input(f"Enter a number (0 to {len(sorted_fridge)-1}) to open the product page: "))
#         if 0 <= number < len(sorted_fridge):
#             product_url = sorted_fridge.iloc[number]["Link"]  # Use the correct 'Link' column
#             if pd.notna(product_url):  # Check if URL exists
#                 print(f"Opening: {product_url}")
#                 webbrowser.open(product_url)
#             else:
#                 print("No URL available for this product.")
#         else:
#             print("Invalid number. Please enter a valid index.")
#     except ValueError:
#         print("Invalid input. Please enter a number.")



# def search_TV(search_term):
#     # Load the Excel files with source names
#     files = {"tv_croma.xlsx": "Croma", "tv_ebay.xlsx": "Ebay"}
    
#     df_list = []
#     for file, source in files.items():
#         df = pd.read_excel(file)
#         df["Website"] = source  # Add a website column
#         df_list.append(df)
    
#     # Combine all DataFrames
#     df = pd.concat(df_list, ignore_index=True)
    
#     # Ensure the 'Link' column exists in the DataFrame
#     if "Link" not in df.columns:
#         print("Error: 'Link' column not found in the Excel file.")
#         return
    
#     # Filter the DataFrame based on the search term (case-insensitive)
#     filtered_tv = df[df["Name"].str.contains(search_term, case=False, na=False)].copy()  # Explicit copy to avoid warnings
    
#     # Clean the 'Price' column (remove currency symbols and commas) and convert to float
#     filtered_tv.loc[:, "Price"] = (
#         filtered_tv["Price"]
#         .astype(str)                      # Ensure it's a string
#         .str.replace(r"[^\d.]", "", regex=True)  # Remove non-numeric characters except dots
#         .astype(float)                    # Convert to float
#     )

#     # Remove rows where price conversion failed
#     filtered_tv = filtered_tv.dropna(subset=["Price"])

#     # Sort the filtered results by Price (ascending)
#     sorted_tv = filtered_tv.sort_values(by=["Price"], ascending=True).reset_index(drop=True)
    
#     # Display results
#     if sorted_tv.empty:
#         print("No TVs found matching your search.")
#         return
    
#     print(sorted_tv[["Price", "Name", "Website", "Link"]])  # Display links in output

#     visualize_data(sorted_tv, search_term)
    
#     try:
#         number = int(input(f"Enter a number (0 to {len(sorted_tv)-1}) to open the product page: "))
#         if 0 <= number < len(sorted_tv):
#             product_url = sorted_tv.iloc[number]["Link"]  # Use the correct 'Link' column
#             if pd.notna(product_url):  # Check if URL exists
#                 print(f"Opening: {product_url}")
#                 webbrowser.open(product_url)
#             else:
#                 print("No URL available for this product.")
#         else:
#             print("Invalid number. Please enter a valid index.")
#     except ValueError:
#         print("Invalid input. Please enter a number.")






# def search_mobile(search_term):
#     # Load the Excel files with source names
#     files = {"mobile_croma.xlsx": "Croma", "mobile_ebay.xlsx": "Ebay"}
    
#     df_list = []
#     for file, source in files.items():
#         df = pd.read_excel(file)
#         df["Website"] = source  # Add a website column
#         df_list.append(df)
    
#     # Combine all DataFrames
#     df = pd.concat(df_list, ignore_index=True)
    
#     # Ensure the 'Link' column exists in the DataFrame
#     if "Link" not in df.columns:
#         print("Error: 'Link' column not found in the Excel file.")
#         return
    
#     # Filter the DataFrame based on the search term (case-insensitive)
#     filtered_mobile = df[df["Name"].str.contains(search_term, case=False, na=False)].copy()  # Explicit copy to avoid warnings
    
#     # Check if there are results
#     if filtered_mobile.empty:
#         print("No mobiles found matching your search.")
#         return

#     # Clean the 'Price' column (remove currency symbols and commas) and convert to float
#     filtered_mobile["Price"] = (
#         filtered_mobile["Price"]
#         .astype(str)                             # Ensure it's a string
#         .str.replace(r"[^\d.]", "", regex=True)  # Remove non-numeric characters except dots
#     )

#     # Convert Price to float (Handle errors safely)
#     filtered_mobile["Price"] = pd.to_numeric(filtered_mobile["Price"], errors="coerce")  
#     filtered_mobile = filtered_mobile.dropna(subset=["Price"])  # Drop rows where price conversion failed

#     # Sort by price (ascending)
#     sorted_mobile = filtered_mobile.sort_values(by=["Price"], ascending=True).reset_index(drop=True)
    
#     if sorted_mobile.empty:
#         print("No mobiles found with valid price data.")
#         return
    
#     print(sorted_mobile[["Price", "Name", "Website", "Link"]])  # Display links in output
    
#     visualize_data(sorted_mobile, search_term)
    
#     try:
#         number = int(input(f"Enter a number (0 to {len(sorted_mobile)-1}) to open the product page: "))
#         if 0 <= number < len(sorted_mobile):
#             product_url = sorted_mobile.iloc[number]["Link"]  
#             if pd.notna(product_url) and isinstance(product_url, str):  # Check if URL exists
#                 print(f"Opening: {product_url}")
#                 webbrowser.open(product_url)
#             else:
#                 print("No valid URL available for this product.")
#         else:
#             print("Invalid number. Please enter a valid index.")
#     except ValueError:
#         print("Invalid input. Please enter a number.")






# def search_headphone(search_term):
#     # Load the Excel files with source names
#     files = {"wireless headphones_croma.xlsx": "Croma", "wireless headphones_ebay.xlsx": "Ebay"}
    
#     df_list = []
#     for file, source in files.items():
#         df = pd.read_excel(file)
#         df["Website"] = source  # Add a website column
#         df_list.append(df)
    
#     # Combine all DataFrames
#     df = pd.concat(df_list, ignore_index=True)
    
#     # Ensure the 'Link' column exists in the DataFrame
#     if "Link" not in df.columns:
#         print("Error: 'Link' column not found in the Excel file.")
#         return
    
#     # Filter the DataFrame based on the search term (case-insensitive)
#     filtered_headphone = df[df["Name"].str.contains(search_term, case=False, na=False)].copy()  # Explicit copy to avoid warnings
    
#     # Check if there are results
#     if filtered_headphone.empty:
#         print("No headphones found matching your search.")
#         return

#     # Clean the 'Price' column (remove currency symbols and commas) and convert to float
#     filtered_headphone["Price"] = (
#         filtered_headphone["Price"]
#         .astype(str)                             # Ensure it's a string
#         .str.replace(r"[^\d.]", "", regex=True)  # Remove non-numeric characters except dots
#     )

#     # Convert Price to float (Handle errors safely)
#     filtered_headphone["Price"] = pd.to_numeric(filtered_headphone["Price"], errors="coerce")  
#     filtered_headphone = filtered_headphone.dropna(subset=["Price"])  # Drop rows where price conversion failed

#     # Sort by price (ascending)
#     sorted_headphone = filtered_headphone.sort_values(by=["Price"], ascending=True).reset_index(drop=True)
    
#     if sorted_headphone.empty:
#         print("No headphones found with valid price data.")
#         return
    
#     print(sorted_headphone[["Price", "Name", "Website", "Link"]])  # Display links in output
#     visualize_data(sorted_headphone, search_term)
#     try:
#         number = int(input(f"Enter a number (0 to {len(sorted_headphone)-1}) to open the product page: "))
#         if 0 <= number < len(sorted_headphone):
#             product_url = sorted_headphone.iloc[number]["Link"]  
#             if pd.notna(product_url) and isinstance(product_url, str):  # Check if URL exists
#                 print(f"Opening: {product_url}")
#                 webbrowser.open(product_url)
#             else:
#                 print("No valid URL available for this product.")
#         else:
#             print("Invalid number. Please enter a valid index.")
#     except ValueError:
#         print("Invalid input. Please enter a number.")






if __name__ == "__main__":

    print('Write 1 to search laptop..')
    print('Write 2 to search fridge..')
    print('Write 3 to search tv..')
    choice = int(input('Enter the choice : '))
    if(choice==1) :
        search_term = input("Enter laptop name: ")
        search_laptop(search_term)
    elif (choice==2) :
        search_term = input("Enter fridge name: ")
        search_Fridge(search_term)
    elif (choice==3) :
        search_term = input("Enter tv name: ")
        search_TV(search_term)
    else :
        print('Invalid choice  plz try again')
    