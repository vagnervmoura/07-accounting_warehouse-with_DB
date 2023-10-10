"""
def load_balance(balance="../db/balance.txt"):
    with open(balance, "a") as file:  # To create a new file in case it not exist.
        pass

    with open(balance) as file:
        for row in file:
            account = float(row)
            #print(account)
    return
load_balance()
"""