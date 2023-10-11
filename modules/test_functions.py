import sys
sys.path.append("database")
import database as new_balance
print(new_balance.load_balance)
from database import load_balance

def f_balance(): 
    global v_balance
    global v_review
    global actual_balance
    global balance
#    with open(balance, "r") as file:
#        for row in file:
#            actual_balance = float(row)
    try:
        load_balance()
#        print(actual_balance)
        v_action = int(input("Press '1' to Add or press '2' to Subtract: "))
        if v_action != 1 and v_action != 2:
            print("Sorry {} is not a valid option.\n".format(v_action))
        else:
            v_value = float(input("Insert the amount to your balance: "))
            if v_action == 1:
                actual_balance += v_value
                #v_balance += v_value
                print("Your new balance is: {}".format(actual_balance))
                v_review.append("Balance changed, added: {}".format(v_value))
            elif v_action == 2:
                if v_value <= actual_balance:
                    actual_balance -= v_value
                    print("Your new balance is: {}".format(actual_balance))
                    v_review.append("Balance changed, subtracted: {}".format(v_value))
                else:
                    print("Sorry, you do not have balance enough to do this withdraw.\nYour actual balance is {}.".format(v_balance))
            new_balance = str(actual_balance) # save the balance as string to send to DB File.
            with open(balance, "w") as file:  # To create a new file in case it not exist and write on.
                file.write(new_balance)
                file.close()
    except ValueError:
        print("Sorry {} is not a valid value.\n".format(v_value))