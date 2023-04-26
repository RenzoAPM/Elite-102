import os
import mysql.connector
from getpass import getpass

connection = mysql.connector.connect(user='root',database='bank',password=getpass())
database = connection.cursor()

'''
History - Date, Type, Amount, ID, AccountID, TargetAccountID
Users - ID, Name, balance, pin, DateCreated, AccountType, Status
'''


'''
    Functions and Options
'''

def sign_in():
    os.system("clear")
    print("===========BANK===========")
    accountid = input("Account ID: ")
    accountpin = input("Account pin: ")
    database.execute(f"select status from users where accountid=%s and pin=%s", (accountid, accountpin))
    if database.fetchone():
        signed_in = True
        while signed_in:
            signed_in = action_menu(accountid)
    else:
        os.system("clear")
        input("""===========BANK===========
** Incorrect ID or pin **
Press enter to go back.
==========================
""")

def new_user():
    os.system("clear")
    print("===========BANK===========")
    accountname = input("Your name: ")
    accountpin = input("Your pin: ")
    database.execute("insert into users (name, pin) values (%s, %s)", (accountname, accountpin))
    database.execute("select accountid from users where accountid=last_insert_id()")
    accountid = database.fetchone()[0]
    connection.commit()
    input(f"Your account ID is: {accountid}\nRemember it.\nPress enter to continue.")

def deposit(account_id):
    os.system("clear")
    print("===========BANK===========\nDeposit some money.")
    needs_number = True
    while needs_number:
        amount = input("Amount to deposit: ")
        # Check if it's a number with only one "." and isn't too long
        if amount.replace(".", "", 1).isdigit():
            amounts = amount.split(".")
            # Check if too many numbers are after the "."
            if len(amounts) == 2:
                if len(amounts[1]) <= 2:
                    if len(amounts[0]) <= 9:
                        needs_number = False
                    else:
                        print("No billionaires.")
                else:
                    print("Only 0.01 precision.")
            else:
                if len(amount) <= 9:
                    needs_number = False
                else:
                    print("No billionaires.")
        else:
            print("That's not a number.")
    input(float(amount))
    database.execute("update users set balance = balance + %s where accountid = %s", (float(amount), account_id))
    connection.commit()
    return 0

def withdraw(account_id, transfer = False):
    if not transfer:
        os.system("clear")
        print("===========BANK===========\nWithdraw some money.")
    # Check the balance
    database.execute(f"select balance from users where accountid={account_id}")
    balance = database.fetchone()[0]
    needs_number = True
    while needs_number:
        if transfer:
            amount = input("Amount to transfer: ")
        else:
            amount = input("Amount to withdraw: ")
        # Check if it's a number with only one "." and isn't too long
        if amount.replace(".", "", 1).isdigit():
            amounts = amount.split(".")
            # Check if too many numbers are after the "."
            if len(amounts) == 2:
                if len(amounts[1]) <= 2:
                    if float(amount) <= float(balance):
                        needs_number = False
                    else:
                        print("You don't have that much.")
                else:
                    print("Only 0.01 precision.")
            else:
                if float(amount) <= float(balance):
                    needs_number = False
                else:
                    print("You don't have that much.")
        else:
            print("That's not a number.")
    database.execute("update users set balance = balance - %s where accountid = %s", (float(amount), account_id))
    connection.commit()
    if transfer:
        return float(amount)
    return 0

def transfer(account_id):
    os.system("clear")
    print("===========BANK===========\nTransfer some money.")
    target_id = input("Recipient account ID: ")
    database.execute(f"select status from users where accountid={account_id}")
    if database.fetchone():
        amount = withdraw(account_id, True)
        database.execute("update users set balance = balance + %s where accountid = %s", (float(amount), target_id))
        connection.commit()
        input("Transfer complete.\nPress enter to continue.")
    else:
        input("No account found.\nPress enter to continue.")
    return 0

def check_balance(account_id):
    os.system("clear")
    database.execute(f"select format(balance, 2) from users where accountid={account_id}")
    balance = database.fetchone()[0]
    input(f"""===========BANK===========
Your balance is ${balance}
Press enter to continue.
==========================
""")
    return 0

def edit_details(account_id):
    return 0

def admin():
    return 0


'''
    Pages
'''

def take_answer(options):
    answer = input("Select option: ")
    if answer not in options:
        print(f"That is not an option.\nOptions are {options}")
    while answer not in options:
        answer = input("Select option: ")
    return answer

def mainpage():
    # Main menu
    # Options are Deposit, Withdraw, Transfer, or Admin.

    # Setting up window
    os.system("clear")
    print("""===========BANK===========
1 - Sign in
2 - Create Account
==========================""")

    answer = take_answer(['1', '2'])

    if answer == '1':
        sign_in()
    else:
        new_user()

'''
    Menu
'''

def action_menu(account_id):

    os.system("clear")
    print("""===========BANK===========
1 - Deposit
2 - Withdraw
3 - Transfer
4 - Check Balance
5 - Edit Account
C - Logout
==========================""")

    answer = take_answer(['1', '2', '3', '4', '5', 'C'])

    if answer == '1':
        deposit(account_id)
        return True
    elif answer == '2':
        withdraw(account_id)
        return True
    elif answer == '3':
        transfer(account_id)
        return True
    elif answer == '4':
        check_balance(account_id)
        return True
    elif answer == '5':
        edit_details(account_id)
        return True
    else:
        return False


def main():
    while True:
        mainpage()


main()
connection.close()
