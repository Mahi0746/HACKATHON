import pandas as pd
import Ready.croma as croma
import Ready.vijay as vijay
import Ready.Poojara as poojara
from Ready.Final_Reccomend import search


# def admin_login():

#     admin_password = "1234"
#     input_password = input("Enter Admin Password: ")
    
#     if input_password == admin_password:
#         print("Login Successful! Welcome, Admin.")
#         admin_panel()
#     else:
#         print("Invalid credentials. Access Denied.")

# def admin_panel():
#     while True:
#         print("\nAdmin Panel:")
#         print("1. View Data")
#         print("2. Update Data")
#         print("3. Logout")
        
#         choice = input("Enter your choice: ")
        
#         if choice == "1":
#             view_data()
#         elif choice == "2":
#             update_data()
#         elif choice == "3":
#             print("Logging out...")
#             break
#         else:
#             print("Invalid choice. Please try again.")

def view_data():
    print("\nAvailable Datasets:")
    files = ["laptop_croma.xlsx", "laptop_ebay.xlsx", "fridge_croma.xlsx", "fridge_ebay.xlsx", "tv_croma.xlsx", "tv_ebay.xlsx","mobile_croma.xlsx","mobile_ebay.xlsx","wireless headphones_croma.xlsx","wireless headphones_ebay.xlsx"]
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    try:
        file_choice = int(input("Select a file to view (enter number): "))
        if 1 <= file_choice <= len(files):
            df = pd.read_excel(files[file_choice - 1])
            print("First 5 rows of file are")
            print(df.head())
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def update_data():
    search_item = input("Enter the product category to update (e.g., laptop, fridge, tv): ")
    print("Updating data...")
    croma.main(search_item)
    # vijay.main(search_item)
    print("Data update completed.")

def user_login():
    print("\nWelcome, User!")
    user_portal()

def user_portal(search_term):
    # while True:
        # print("\nUser Portal:")
        # print("1. Search Item")
        # print("2. Search Fridge")
        # print("3. Search TV")
        # print("4. Search Mobile")
        # print("5. Search Headphones")
        # print("0. Exit")
        
        # choice = input("Enter your choice: ")
        
        # if choice == "1":
            # search_term = input("Enter search item name: ")
            # flag1 = False
            # flag2 = False
            # vijay.main(search_term)
        croma.main(search_term)
        vijay.main(search_term)
        poojara.scrape_poojaratele(search_term)
        search(search_term)
        # elif choice == "2":
        #     search_term = input("Enter fridge name: ")
        #     search_Fridge(search_term)
        # elif choice == "3":
        #     search_term = input("Enter TV name: ")
        #     search_TV(search_term)
        # elif choice == "4":
        #     search_term = input("Enter Mobile name: ")
        #     search_mobile(search_term)
        # elif choice == "5":
        #     search_term = input("Enter Headphone name: ")
        #     search_headphone(search_term)
        # elif choice == "0":
        #     print("Exiting user portal...")
        #     break
        # else:
        #     print("Invalid choice. Please try again.")
    
# if __name__ == "__main__":
#     print("Welcome to the Ecommerce Analysis System")
#     print("1. Login as Admin")
#     print("2. Login as User")

#     choice = int(input("enter your choice: ") )
#     if choice == 1:
#         admin_login()
#     else:
#         user_login()

#  graph 

# user_portal()