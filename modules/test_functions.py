


def save_balance(balance="../db/balance.txt"):
    with open(balance, "w") as file:  # To create a new file in case it not exist.
        file.write(v_balance)



    
#save_balance()