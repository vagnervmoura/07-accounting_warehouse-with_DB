def new_review():
    """{'2023-01-01': ["transaction", "v_value"]}"""
    from datetime import datetime
#    from main_test_account_with_database import f_review
    import main_test_account_with_database
#    from main_test_account_with_database import f_balance.price
#    from main_test_account_with_database import price
    review = "db/review.txt" # Set review history to a Database File
    review_dict = {}
    main_test_account_with_database.f_balance.v_trans
    with open(review, "r") as file:

        print("PRIMEIRO")
        for row in file:
            date_transaction, transaction, price = row.strip().split(";")
            if date_transaction not in review_dict:
                review_dict[date_transaction] = []
    print(review_dict)
    with open(review, "a") as file:
        print("SEGUNDO")
        date_transaction = datetime.now()
        date_time_transaction = date_transaction.strftime('%Y/%m/%d %H:%M')
        file.write(f"{date_time_transaction};{transaction};{price}\n")
    file.close()   

#v_review.append("Balance changed, subtracted: {}".format(v_value))



"""
def new_review():
    {'2023-01-01': ["transaction", "v_value"]}
    from datetime import datetime
    from main_test_account_with_database import v_transaction
    from main_test_account_with_database import price
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
#        transaction = v_transaction
        file.write(f"{date_time_transaction};{transaction};{price}\n")
    file.close()   

#v_review.append("Balance changed, subtracted: {}".format(v_value))
"""