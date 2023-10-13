# 07-accounting-system-warehouse-with-text-database
"""
In this exercise, you'll extend the functionality of the company account and warehouse operations program from the previous lesson. 
You'll implement: 
saving and loading of: 
   V - account balance, 
    - warehouse inventory, and 
    - operation history 
to/from a text file.

1. You can store balance, inventory and history in separate files or in one file.

2. At the start of the program, if the file(s) exists, load the data from the file and use it to initialize the program state.
  - If the file does not exist or if there are any errors during file reading (e.g., the file is corrupted or not readable), handle these cases gracefully.
  - Make sure to save all the data to correct files when the program is being shutdown.

Hints:
- Use built-in Python functions for file I/O and converting data to Python objects (i.e. literal_eval).
- Remember to handle any file I/O errors that may occur.
- Think about the format in which you'll save the data to the file. The format should be easy to read back into the program.
- Always close the files after you're done with them to free up system resources.
"""
#print('\033[1m' + "NEGRITO" + '\033[0m')

import sys
from datetime import datetime
#from modules.test_functions import save_balance
#from modules.database import load_balance

v_option = None
v_balance = 0
v_sale = 0
v_purchase = []
v_account = 0
v_list = None
v_quantity = 0
v_warehouse = []
v_review = []
#from modules.database import actual_balance
from test_functions import new_review

balance="db/balance.txt" # Set balance from a Database File
warehouse="db/warehouse.txt" # Set warehouse to Database File
review = "db/review.txt" # Set review history to a Database File

def goto(linenum):
    global line
    line = linenum


# 'balance': The program will prompt for an amount to add or subtract from the account.
def f_balance(): 
    global v_balance
    global v_review
    
    with open(balance, "r") as file:
        for row in file:
            actual_balance = float(row)         
    try:
        v_action = int(input("Press '1' to Add or press '2' to Subtract: "))
        if v_action != 1 and v_action != 2:
            print("Sorry {} is not a valid option.\n".format(v_action))
        else:
            v_value = float(input("Insert the amount to your balance: "))
            price = v_value
            if v_action == 1:
                actual_balance += v_value
                print("Your new balance is: {}".format(actual_balance))
                v_review.append("Balance changed, Add {}".format(v_value))
                v_transaction = "Account Add"
                   
            elif v_action == 2:
                if v_value <= actual_balance:
                    actual_balance -= v_value
                    print("Your new balance is: {}".format(actual_balance))
                    v_review.append("Balance changed, Sub: {}".format(v_value))
                    v_transaction = "Account Sub"
                
                else:
                    print("Sorry, you do not have balance enough to do this withdraw.\nYour actual balance is {}.".format(v_balance))
            new_balance = str(actual_balance) # save the balance as string to send to DB File.
            with open(balance, "w") as file:  # To create a new file in case it not exist and write on.
                file.write(new_balance)
                file.close()
            

            """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
            review = "db/review.txt" # Set review history to a Database File
            review_dict = {}
            with open(review, "r") as file:
                for row in file:
                    date_transaction, transaction, v_value = row.strip().split(";")
                    if date_transaction not in review_dict:
                        review_dict[date_transaction] = []
            print(review_dict)
            with open(review, "a") as file:
                date_transaction = datetime.now()
                date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M')
                transaction = v_transaction
                file.write(f"{date_time_transaction};{transaction};{price}\n")
            file.close()   

    except ValueError:
        print("Sorry {} is not a valid value.\n".format(v_value))


# 'sale': The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly.        
def f_sale():
    global v_sale
    global v_balance
    global v_quantity
    global v_warehouse
    global v_review

    with open(balance, "r") as file:
        for row in file:
            actual_balance = float(row)

    new_warehouse = {}  
    with open(warehouse, "a") as file: # To create a new file in case it not exist.
        pass 
    with open(warehouse) as file:
        for row in file:
            v_name, v_price, v_quantity = row.strip().split(";")
            v_price = float(v_price)
            v_quantity = int(v_quantity)
            if v_name in new_warehouse:
                print(f"WARNING: duplicate value of {v_name}")
            new_warehouse[v_name] = {
                "v_price": v_price,
                "v_quantity": v_quantity
            }
    print(new_warehouse)
            
    try:
        s_name = str(input("Insert the name of product: "))
        if (s_name not in new_warehouse):# or (new_warehouse["v_quantity"] <1):
            print("Sorry, {} not available on Warehouse.\n".format(s_name))
            return
        s_quantity = int(input("Insert the quantity of {} to sell: ".format(v_name)))
        if s_quantity > new_warehouse[s_name]["v_quantity"]:
            print("Sorry, you do not have enough {} to sell.\n".format(v_name))
            return
        new_warehouse[s_name]["v_quantity"] -= s_quantity
        total_price = new_warehouse[s_name]["v_price"] * s_quantity
        actual_balance += total_price
        if new_warehouse[s_name]["v_quantity"] == 0:
            del(new_warehouse[s_name])
            print(f"Last {s_name} sold, deleting from warehouse.")
        
        new_balance = str(actual_balance) # save the balance as string to send to DB File.
        with open(balance, "w") as file:  # To create a new file in case it not exist and write on.
            file.write(new_balance)
            file.close()
        with open(warehouse, "w") as file:  # To create a new file in case it not exist and write on.
            for v_name, stats in new_warehouse.items():
                file.write("{};{};{}\n".format(v_name, stats["v_price"], stats["v_quantity"]))
            file.close()

            
        """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
        price = total_price
        v_transaction = "Sale "+str(s_quantity)+" product: "+s_name+" by"
        review = "db/review.txt" # Set review history to a Database File
        review_dict = {}
        with open(review, "r") as file:
            print("PRIMEIRO")
            for row in file:
                date_transaction, transaction, v_value = row.strip().split(";")
                if date_transaction not in review_dict:
                    review_dict[date_transaction] = []
        print(review_dict)
        with open(review, "a") as file:
            print("SEGUNDO")
            date_transaction = datetime.now()
            date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M')
            transaction = v_transaction
            file.write(f"{date_time_transaction};{transaction};{price}\n")
        file.close()  
            
    except ValueError:
        print("Sorry, you did not input a valid value.\n")
    
# 'purchase': The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly. 
#             Ensure that the account balance is not negative after a purchase operation.    
def f_purchase():
    global v_purchase
    global v_balance
    global v_warehouse
    global v_review
    
    with open(balance, "r") as file:
        for row in file:
            actual_balance = float(row)
    
    new_warehouse = {}  
    with open(warehouse, "a") as file: # To create a new file in case it not exist.
        pass 
    with open(warehouse) as file:
        for row in file:
            v_name, v_price, v_quantity = row.strip().split(";")
            v_price = float(v_price)
            v_quantity = int(v_quantity)
            if v_name in new_warehouse:
                print(f"WARNING: duplicate value of {v_name}")
            new_warehouse[v_name] = {
                "v_price": v_price,
                "v_quantity": v_quantity
            }
    print(new_warehouse)
            
    try:
        v_name = str(input("Insert the name of product: "))
        v_price = float(input("Insert the unit price of {}: ".format(v_name)))
        v_quantity = int(input("Insert the quantity of {}: ".format(v_name)))
        
        total_price = v_price * v_quantity
        if total_price > actual_balance:
            print("Sorry, you do not have balance enough to do this purchase.\nYour actual balance is {}.".format(v_balance))
        else:   
            if v_name not in new_warehouse:
                new_warehouse[v_name] = {"v_price": 0.0, "v_quantity": 0}
            new_warehouse[v_name]["v_price"] = v_price
            new_warehouse[v_name]["v_quantity"] += v_quantity 
            actual_balance -= total_price
        
        new_balance = str(actual_balance) # save the balance as string to send to DB File.
        with open(balance, "w") as file:  # To create a new file in case it not exist and write on.
            file.write(new_balance)
            file.close()
        with open(warehouse, "w") as file:  # To create a new file in case it not exist and write on.
            for v_name, stats in new_warehouse.items():
                file.write("{};{};{}\n".format(v_name, stats["v_price"], stats["v_quantity"]))
            file.close()  
            
            
        """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
        s_name = v_name
        price = total_price
        s_quantity = v_quantity
        v_transaction = "Purchase "+str(s_quantity)+" product: "+s_name+" by"
        review = "db/review.txt" # Set review history to a Database File
        review_dict = {}
        with open(review, "r") as file:
            print("PRIMEIRO")
            for row in file:
                date_transaction, transaction, v_value = row.strip().split(";")
                if date_transaction not in review_dict:
                    review_dict[date_transaction] = []
        print(review_dict)
        with open(review, "a") as file:
            print("SEGUNDO")
            date_transaction = datetime.now()
            date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M')
            transaction = v_transaction
            file.write(f"{date_time_transaction};{transaction};{price}\n")
        file.close()  
                
    except ValueError:
        print("Sorry, you did not input a valid value.\n")

# 'account': Display the current account balance.
def f_account():
    global v_account
    
    with open(balance, "r") as file:
        for row in file:
            actual_balance = float(row)
            
    if v_account == []:
        print("The account is empty.\n")
    else:
        print("Your actual balance is: {}".format(actual_balance))
    file.close()

# 'list': Display the total inventory in the warehouse along with product prices and quantities.
def f_list():
    new_warehouse = {}  
    with open(warehouse, "a") as file: # To create a new file in case it not exist.
        pass 
    with open(warehouse) as file:
        for row in file:
            v_name, v_price, v_quantity = row.strip().split(";")
            v_price = float(v_price)
            v_quantity = int(v_quantity)
            if v_name in new_warehouse:
                print(f"WARNING: duplicate value of {v_name}")
            new_warehouse[v_name] = {
                "v_price": v_price,
                "v_quantity": v_quantity
            }
        if new_warehouse == {}:
            print("\nWarehouse is empty.")
            return

        print("\n\nThe list of products on Warehouse are:")
        for v_name in new_warehouse:
            print("{}: {} itens - Price: {}".format(v_name, new_warehouse[v_name]["v_quantity"], new_warehouse[v_name]["v_price"]))
    file.close()


# 'warehouse': Prompt for a product name and display its status in the warehouse.
def f_warehouse():
    new_warehouse = {}  
    with open(warehouse, "a") as file: # To create a new file in case it not exist.
        pass 
    with open(warehouse) as file:
        for row in file:
            v_name, v_price, v_quantity = row.strip().split(";")
            v_price = float(v_price)
            v_quantity = int(v_quantity)
            if v_name in new_warehouse:
                print(f"WARNING: duplicate value of {v_name}")
            new_warehouse[v_name] = {
                "v_price": v_price,
                "v_quantity": v_quantity
            }
        if new_warehouse == {}:
            print("\nWarehouse is empty.")
            return    
        s_name = str(input("Insert the name of product: "))
        if (s_name not in new_warehouse):
            print("Sorry, {} not available on Warehouse.\n".format(s_name))
            return
        print("\n\nThe {} is Available in Warehouse.\nHave {} itens in Warehouse.\nAnd its price is {}\n".format(s_name, new_warehouse[s_name]["v_quantity"], new_warehouse[s_name]["v_price"]))
    file.close()


# 'review': Prompt for two indices 'from' and 'to', and display all recorded operations within that range. 
#           If ‘from’ and ‘to’ are empty, display all recorder operations. 
#           Handle cases where 'from' and 'to' values are out of range.
def f_review():
    """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
    review = "db/review.txt" # Set review history to a Database File
    review_dict = {}
    with open(review, "r") as file:
        for row in file:
            print(row)
    file.close()       


while v_option != 0:
    v_option = int(input("\n\nSelect one of the following options:\n1 - balance\n2 - sale\n3 - purchase\n4 - account\n5 - list\n6 - warehouse\n7 - review\n0 - end\n\n"))

    try:
        if v_option == 0:
            print("\nThank you for using our system.\n\n")
            exit()
            
        elif v_option == 1: # option to balance
            print("You choose the option {} to check the Balance.".format(v_option))
            f_balance()
            
        elif v_option == 2: # option to sale
            print("You choose the option {} to check the sale.".format(v_option))
            f_sale()
            
        elif v_option == 3: # option to purchase
            print("You choose the option {} to check the purchase.".format(v_option))
            f_purchase() 
                 
        elif v_option == 4: # option to account
            print("You choose the option {} to check the account.".format(v_option))
            f_account()
            
        elif v_option == 5: # option to list
            print("You choose the option {} to check the list.".format(v_option))
            f_list()
            
        elif v_option == 6: # option to warehouse
            print("You choose the option {} to check the warehouse.".format(v_option))
            f_warehouse()
            
        elif v_option == 7: # option to review
            print("You choose the option {} to check the review.".format(v_option))
            f_review() 
                
    except ValueError:
        print("Sorry, but you have input a wrong option, please let's try again with an valid option number.\n")