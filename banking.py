import math
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "number TEXT,"
            "pin TEXT,"
            "balance INTEGER DEFAULT 0);")
conn.commit()
conn.row_factory = sqlite3.Row

login_number = ''
check = True

def visa_id():
    visa_id = list(str(400000))
    return visa_id

def account_creation():
    account_id = luhn_algorithm()
    random_pin = random.randint(0, 9999)
    pin = '{:04d}'.format(random_pin)
    account_database[account_id] = pin
    cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (account_id, pin))
    conn.commit()
    print(f"""
Your card has been created
Your card number:
{account_id}
Your card PIN:
{pin}""")

def account_login():
    global login_number
    login = input("Enter your card number: ")
    password = input("Enter your PIN: ")
    cur.execute('SELECT number, pin FROM card WHERE number and pin in (?, ?)', (login, password))
    found = cur.fetchone()
    if found:
        print("You have successfully logged in!")
        print("Wrong card number or PIN!")
        login_number = login
        inside_account()
    else:
        print("Wrong card number or PIN!")
        
def inside_account():
    while True:
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        choice = int(input())
        if choice == 1:
            print(cur.execute('SELECT balance FROM card WHERE number=?',(login_number,)))
            continue
        elif choice == 2:
            cur.execute('SELECT balance FROM card WHERE number=?', (login_number,))
            account_balance = cur.fetchone()
            income = int(input("Enter income: "))
            new_balance = account_balance[0] + income
            cur.execute('UPDATE card '
                        'SET balance=? '
                        'WHERE number=?', (new_balance, login_number))
            conn.commit()
            print("Income was added!")
            continue
        elif choice == 3:
            cur.execute('SELECT balance FROM card WHERE number=?', (login_number,))
            account_balance = cur.fetchone()
            transfer_number = input('Enter card number: ')
            check_number = list(str(transfer_number))
            luhn_check(check_number)
            if check == False:
                continue
            else:
                cur.execute('SELECT number'
                            ' FROM card '
                            'WHERE number in (?)', (transfer_number,))
                find = cur.fetchone()
                if find:
                    transfer = int(input('Enter how much money you want to transfer: '))
                    if transfer > account_balance[0]:
                        print('Not enough money!')
                        continue
                    else:
                        new_account_balance = account_balance[0] - transfer
                        cur.execute('UPDATE card '
                                    'SET balance=? '
                                    'WHERE number=?', (new_account_balance, login_number))
                        conn.commit()
                        cur.execute('SELECT balance FROM card WHERE number=?', (transfer_number,))
                        transfer_balance = cur.fetchone()
                        new_transfer = transfer + transfer_balance[0]
                        cur.execute('UPDATE card '
                                    'SET balance=? '
                                    'WHERE number=?', (new_transfer, transfer_number))
                        conn.commit()
                        print('Success!')
                        continue
                else:
                    print("Such a card does not exist.")
        elif choice == 4:
            cur.execute('DELETE FROM card WHERE number=?', (login_number,))
            conn.commit()
        elif choice == 5:
            print("You have successfully logged out!")
            break
        else:
            exit()
            
def luhn_algorithm():
    while True:
        random.seed()
        random_account_num = list('{:010d}'.format(random.randrange(9999999999)))
        card_number = visa_id() + random_account_num
        whole_number = visa_id() + random_account_num
        checksum = int(whole_number.pop())
        for x in range(0, len(whole_number)): 
            whole_number[x] = int(whole_number[x]) 
        for x in range(0, len(whole_number)):
            if whole_number[x] == 0:
                whole_number[x] *= 2
            elif x % 2 == 0:
                whole_number[x] *= 2
            else:
                continue
        for x in range(0, len(whole_number)):
            if whole_number[x] > 9:
                whole_number[x] -= 9
            else:
                continue
        whole_number.append(checksum)
        if (sum(whole_number) % 10) != 0:
            continue
        else:
            final = "".join(card_number)
            if final in cur.fetchall():
                continue
            else:
                return final
                break

def luhn_check(check_number):
    checksum = int(check_number.pop())
    for x in range(0, len(check_number)):
        check_number[x] = int(check_number[x])
    for x in range(0, len(check_number)):
        if check_number[x] == 0:
            check_number[x] *= 2
        elif x % 2 == 0:
            check_number[x] *= 2
        else:
            continue
    for x in range(0, len(check_number)):
        if check_number[x] > 9:
            check_number[x] -= 9
        else:
            continue
    check_number.append(checksum)
    if (sum(check_number) % 10) != 0:
        print('Probably you made a mistake in the card number. Please try again!')
        check = False
    
account_database = {}

while True:
    print("""1. Create an account
2. Log into account
0. Exit""")
    option = int(input())
    if option == 1:
        account_creation()
        continue
    elif option == 2:
        account_login()
        continue
    else:
        exit()

conn.commit()
