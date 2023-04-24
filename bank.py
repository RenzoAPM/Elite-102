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
    database.execute(f"select status from users where accountid='{accountid}' and pin='{accountpin}'")
    if len(database.fetchone()):
        signed_in = True
        while signed_in:
            signed_in = action_menu(accountid)
    else:
        os.system("clear")
        input("""===========BANK===========
** Incorect ID or pin **
Press enter to go back.
==========================
""")

def new_user():
    os.system("clear")
    print("===========BANK===========")
    accountname = input("Your name: ")
    accountpin = input("Your pin: ")
    database.execute(f"insert into users (name, pin) values (%s, %s)", (accountname, accountpin))
    database.execute("select accountid from users where accountid=last_insert_id()")
    print(f"Your account ID is: {database.fetchone()[0]}\nRemember it.")
    connection.commit()

def deposit(account_id):

    print("===========BANK===========\nDeposit some money.")
    return 0

def withdraw(account_id):
    return 0

def transfer(account_id):
    return 0

def edit_details(account_id):
    return 0

def admin():
    return 0

def back():
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

    answer = take_answer(['1', '2', '3', '4', 'C'])

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
        edit_details(account_id)
        return True
    else:
        return False



def modify():

    global accountid
    global serialnumber
    global option
    if option == 6:
        global newname
        global newid
        global newcohort
    print(f"Option: {option}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    accountid = accountid.get()
    serialnumber = serialnumber.get()

    commands = [
        f'sshpass -p {password} ssh -t {address} echo {password} | sudo -S mysql -e"insert into history (studentid, time, type, counts, serialnumber) values ({accountid}, \'{now}\', \'checkin\', 1, \'{serialnumber}\'); insert into buffer (studentid, time, type, counts, serialnumber) values ({accountid}, \'{now}\', \'checkin\', 1, \'{serialnumber}\')" beakdb',
        f'sshpass -p {password} ssh -t {address} echo {password} | sudo -S mysql -e"insert into history (studentid, time, type, counts, serialnumber) values ({accountid}, \'{now}\', \'checkin\', 0, \'{serialnumber}\'); insert into buffer (studentid, time, type, counts, serialnumber) values ({accountid}, \'{now}\', \'checkin\', 0, \'{serialnumber}\'); update students set chromebooks = chromebooks - 1 where studentid = {accountid}" beakdb',
        f'sshpass -p {password} ssh -t {address} echo {password} | sudo -S mysql -e"insert into history (studentid, time, type, serialnumber) values ({accountid}, \'{now}\', \'checkout\', \'{serialnumber}\'); insert into buffer (studentid, time, type, serialnumber) values ({accountid}, \'{now}\', \'checkout\', \'{serialnumber}\'); update students set chromebooks = chromebooks + 1, chromebook = \'{serialnumber}\' where studentid = {accountid}" beakdb',
        f'sshpass -p {password} ssh -t {address} echo {password} | sudo -S mysql -e"insert into history (studentid, time, type) values ({accountid}, \'{now}\', \'charger\'); insert into buffer (studentid, time, type) values ({accountid}, \'{now}\', \'charger\'); update students set chargers = chargers + 1 where studentid = {accountid}" beakdb',
        f'sshpass -p {password} ssh -t {address} echo {password} | sudo -S mysql -e"insert into history (studentid, time, type) values ({accountid}, \'{now}\', \'bag\'); insert into buffer (studentid, time, type) values ({accountid}, \'{now}\', \'bag\'); update students set bags = bags + 1 where studentid = {accountid}" beakdb',
        f'sshpass -p {password} ssh -t {address} echo {password} | sudo -S mysql -e"insert into students (studentid, name, cohort, chromebook, chromebooks, chargers, bags, new) values ({int(newid.get())}, \'{newname.get()}\', {int(newcohort.get())}, \'{serialnumber}\', 1, 1, 1, 1); insert into history (studentid, time, type, serialnumber) values ({int(newid.get())}, \'{now}\', \'checkout\', \'{serialnumber}\'); insert into buffer (studentid, time, type, serialnumber) values ({int(newid.get())}, \'{now}\', \'checkout\', \'{serialnumber}\'); insert into history (studentid, time, type) values ({int(newid.get())}, \'{now}\', \'charger\'); insert into buffer (studentid, time, type) values ({int(newid.get())}, \'{now}\', \'charger\');" beakdb'
    ]

    os.system(commands[option-1])
    back()


def main():
    while True:
        mainpage()


main()
connection.close()
