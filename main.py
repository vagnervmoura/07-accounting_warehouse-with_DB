import sys
from datetime import datetime
import ast  # For literal_eval

# File paths
balance_file = "db/balance.txt"
warehouse_file = "db/warehouse.txt"
review_file = "db/review.txt"


def create_files():
    with open(balance_file, "a") as file: # To create a new file in case it not exist.
        pass

    with open(warehouse_file, "a") as file: # To create a new file in case it not exist.
        pass

    with open(review_file, "a") as file: # To create a new file in case it not exist.
        pass

def load_data():
    try:
        with open(balance_file, "r") as file:
            v_balance = float(file.read().strip())
    except (FileNotFoundError, ValueError):
        print("Error loading balance file. Initializing balance to 0.")
        v_balance = 0

    try:
        with open(warehouse_file, "r") as file:
            v_warehouse = ast.literal_eval(file.read().strip())
    except (FileNotFoundError, ValueError, SyntaxError):
        print("Error loading warehouse file. Initializing warehouse to empty.")
        v_warehouse = {}

    try:
        with open(review_file, "r") as file:
            v_review = ast.literal_eval(file.read().strip())
    except (FileNotFoundError, ValueError, SyntaxError):
        print("Error loading review file. Initializing review to empty.")
        v_review = []

    return {"v_balance": v_balance, "v_warehouse": v_warehouse, "v_review": v_review}

def save_data(data):
    try:
        # Save balance to file
        with open(balance_file, "w") as file:
            file.write(str(data["v_balance"]))

        # Save warehouse inventory to file
        with open(warehouse_file, "w") as file:
            file.write(str(data["v_warehouse"]))

        # Save operation history to file
        with open(review_file, "w") as file:
            file.write(str(data["v_review"]))
    except Exception as e:
        print(f"Error saving data to files: {e}")


# 'balance': The program will prompt for an amount to add or subtract from the account.
def f_balance(data):
    v_balance = data.get("v_balance", 0)  # Initialize v_balance to 0 if it doesn't exist in the data dictionary
#    v_review = data.get("v_review", [])  # Initialize v_review to an empty list if it doesn't exist in the data dictionary

    actual_balance = v_balance if v_balance else 0  # Initialize actual_balance to v_balance or 0 if it's empty

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
                v_transaction = "Added to Account"
            elif v_action == 2:
                if v_value <= actual_balance:
                    actual_balance -= v_value
                    print("Your new balance is: {}".format(actual_balance))
                    v_transaction = "Withdraw from Account"
                else:
                    print("Sorry, you do not have a balance enough to do this withdraw.\nYour actual balance is {}.".format(v_balance))

            data["v_balance"] = actual_balance  # Update the balance in the data dictionary

            """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
            review = data.get("v_review", [])
            price = v_value
            v_transaction = "Added to Account"
            date_transaction = datetime.now()
            date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M:%S')
            transaction = v_transaction
            review.append(f"{date_time_transaction};{transaction};{price}")

            data["v_review"] = review

            # Save the updated data
            save_data(data)

    except ValueError:
        print("Sorry {} is not a valid value.\n".format(v_value))

    return data

#    return {"v_balance": actual_balance, "v_review": v_review}


# 'sale': The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly.
def f_sale(data):
    v_balance = data.get("v_balance", 0)
    v_sale = data.get("v_sale", 0)
    v_warehouse = data.get("v_warehouse", {})
    v_review = data.get("v_review", [])

    if not v_warehouse:
        print("\nYour warehouse is empty, and you cannot do any sale.")
        return data

    try:
        s_name = str(input("Insert the name of the product: "))
        if s_name not in v_warehouse:
            print("Sorry, {} not available in the warehouse.\n".format(s_name))
            return data

        s_quantity = int(input("Insert the quantity of {} to sell: ".format(s_name)))
        if s_quantity > v_warehouse[s_name]["v_quantity"]:
            print("Sorry, you do not have enough {} to sell.\n".format(s_name))
            return data

        total_price = v_warehouse[s_name]["v_price"] * s_quantity
        v_sale += total_price
        v_warehouse[s_name]["v_quantity"] -= s_quantity

        if v_warehouse[s_name]["v_quantity"] == 0:
            del v_warehouse[s_name]
            print(f"Last {s_name} sold, deleting from the warehouse.")

        with open(balance_file, "r") as file:
            for row in file:
                actual_balance = float(row)
        actual_balance += total_price

        data["v_balance"] = actual_balance
        data["v_sale"] = v_sale
        data["v_warehouse"] = v_warehouse

        """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
        review = data.get("v_review", [])
        price = total_price
        v_transaction = "Sale {} product: {} by".format(s_quantity, s_name)
        date_transaction = datetime.now()
        date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M:%S')
        transaction = v_transaction
        review.append(f"{date_time_transaction};{transaction};{price}")

        data["v_review"] = review

        # Save the updated data
        save_data(data)

    except ValueError:
        print("Sorry, you did not input a valid value.\n")

    return data


# 'purchase': The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly.
#             Ensure that the account balance is not negative after a purchase operation.
def f_purchase(data):
    v_purchase = data.get("v_purchase", [])
    v_balance = data.get("v_balance", 0)
    actual_balance = data.get("v_balance", 0.0)
    v_warehouse = data.get("v_warehouse", [])
    v_review = data.get("v_review", [])

    with open(balance_file, "r") as file:
        for row in file:
            actual_balance = float(row)
        actual_balance = v_balance if v_balance else 0
        if actual_balance == 0.0:
            print("\nYour account is empty and you can not do any purchase.")
            return
        elif actual_balance <= 0:
            print("\nYour account is empty and you can not do any purchase.")
            return

    try:
        v_name = str(input("Insert the name of product: "))
        v_price = float(input("Insert the unit price of {}: ".format(v_name)))
        v_quantity = int(input("Insert the quantity of {}: ".format(v_name)))

        total_price = v_price * v_quantity
        if total_price > actual_balance:
            print("Sorry, you do not have a balance enough to do this purchase.\nYour actual balance is {}.".format(actual_balance))
        else:
            if v_name not in v_warehouse:
                v_warehouse[v_name] = {"v_price": 0.0, "v_quantity": 0}
            v_warehouse[v_name]["v_price"] = v_price
            v_warehouse[v_name]["v_quantity"] += v_quantity
            actual_balance -= total_price

        data["v_balance"] = actual_balance
        data["v_warehouse"] = v_warehouse

        """{'YYYY-MM-DD HH:MM': ["transaction", "v_value"]}"""
        review = data.get("v_review", [])
        s_name = v_name
        price = total_price
        s_quantity = v_quantity
        v_transaction = "Purchase {} product: {} by".format(s_quantity, s_name)
        date_transaction = datetime.now()
        date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M:%S')
        transaction = v_transaction
        review.append(f"{date_time_transaction};{transaction};{price}")

        data["v_review"] = review

        # Save the updated data
        save_data(data)

    except ValueError:
        print("Sorry, you did not input a valid value.\n")

    return data


# 'account': Display the current account balance.
def f_account(data):
    actual_balance = []
    with open(balance_file, "a") as file:  # To create a new file in case it does not exist.
        pass
    with open(balance_file) as file:
        for row in file:
            actual_balance = float(row)

        if (actual_balance == []) or (actual_balance == 0):
            print("The account is empty.\n")
        else:
            print("Your current balance is: {}".format(actual_balance))
        file.close()

    return {"v_balance": actual_balance, "v_review": data["v_review"]}

def f_list(data):

    with open(balance_file, "a") as file: # To create a new file in case it not exist.
        pass

    v_warehouse = data["v_warehouse"]

    new_warehouse = v_warehouse.copy()  # Create a copy to avoid modifying the original data

    if not new_warehouse:
        print("\nWarehouse is empty.")
        return data  # Return the unmodified data dictionary

    print("\n\nThe list of products in the Warehouse is:")
    for v_name in new_warehouse:
        print("{}: {} items - Price: {}".format(v_name, new_warehouse[v_name]["v_quantity"], new_warehouse[v_name]["v_price"]))

    return data  # Return the unmodified data dictionary

def f_warehouse(data):
    v_warehouse = data["v_warehouse"]

    new_warehouse = v_warehouse.copy()  # Create a copy to avoid modifying the original data

    if not new_warehouse:
        print("\nWarehouse is empty.")
        return data  # Return the unmodified data dictionary

    s_name = input("Insert the name of the product: ")

    if s_name not in new_warehouse:
        print("Sorry, {} not available in Warehouse.\n".format(s_name))
        return data  # Return the unmodified data dictionary

    print("\n\nThe {} is available in Warehouse.".format(s_name))
    print("Have {} items in Warehouse.".format(new_warehouse[s_name]["v_quantity"]))
    print("And its price is {}\n".format(new_warehouse[s_name]["v_price"]))

    return data  # Return the unmodified data dictionary

def f_review(data):
    v_review = data["v_review"]

    review_dict = {}  # Initialize an empty dictionary to hold the review data

    if not v_review:
        print("\nReview file is empty.\n")
        return data  # Return the unmodified data dictionary

    for row in v_review:
        date_transaction, transaction, v_value = row.strip().split(";")
        review_dict[date_transaction] = {
            "transaction": transaction,
            "v_value": v_value
        }

    for date_transaction in review_dict:
        print("{} - {} - {}".format(date_transaction, review_dict[date_transaction]["transaction"], review_dict[date_transaction]["v_value"]))

    return data  # Return the unmodified data dictionary

# Initialize data
create_files()
data = load_data()

while True:
    v_option = int(input("\n\nSelect one of the following options:\n1 - balance\n2 - sale\n3 - purchase\n4 - account\n5 - list\n6 - warehouse\n7 - review\n0 - end\n\n"))

    try:
        if v_option == 0:
            save_data(data)  # Save data before exiting
            print("\nThank you for using our system.\n\n")
            exit()

        elif v_option == 1:  # option to balance
            print("You choose the option {} to check the Balance.".format(v_option))
            data = f_balance(data)

        elif v_option == 2:  # option to sale
            print("You choose the option {} to check the sale.".format(v_option))
            data = f_sale(data)

        elif v_option == 3:  # option to purchase
            print("You choose the option {} to check the purchase.".format(v_option))
            data = f_purchase(data)

        elif v_option == 4:  # option to account
            print("You choose the option {} to check the account.".format(v_option))
            data = f_account(data)

        elif v_option == 5:  # option to list
            print("You choose the option {} to check the list.".format(v_option))
            data = f_list(data)

        elif v_option == 6:  # option to warehouse
            print("You choose the option {} to check the warehouse.".format(v_option))
            data = f_warehouse(data)

        elif v_option == 7:  # option to review
            print("You choose the option {} to check the review.".format(v_option))
            data = f_review(data)

    except ValueError:
        print("Sorry, but you have input a wrong option, please let's try again with a valid option number.\n")