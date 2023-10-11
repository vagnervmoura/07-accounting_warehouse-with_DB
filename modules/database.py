#actual_balance = float(0)

def load_balance(balance="./db/balance.txt"):
#    global actual_balance
#    with open(balance, "a") as file:  # To create a new file in case it not exist.
#        pass
    with open(balance, "r") as file:
        for row in file:
            actual_balance = float(row)
            #print(actual_balance)
    return actual_balance
#load_balance()


"""
balance="../db/balance.txt"
def load_balance():
#    balance = "../db/blance.txt"
    print(balance)
    with open(balance, "r") as file:
        for row in file:
            actual_balance = float(row)
            print(actual_balance)
"""