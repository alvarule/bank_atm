"""
- try-except is used where there is possibility of generation of error when taking inputs from user
- while loops are used for convenience like if something invalid happened
    then instead of exiting the function it'll just execute it from the beginning

* Files - (The program will auto create the required files, So no need to create any file manually)

2 main files (required) -
    1 - list_of_acc.txt - stores list of all existing Account's details file i.e. <account_no>.txt
    2 - deleted_acc_no.txt - stores all deleted account's number
2 files for each created Account -
    1 for storing account details which will be used when exporting when program reruns &
    1 for statement of transactions (withdraw, deposit and money transfer) made on the account

* Logic of Program -

- First of all, existence of 2 files will be checked ( list_of_acc.txt, deleted_acc_no.txt ) and if they are not existing
    then they will be created.
- After that it'll check for existing accounts in list_of_acc.txt file and if it founds any entry it will import that acc
- If it doesn't find any existing acc, it'll ask user to create acc first
- then it'll ask to select acc from the list of all accounts with PIN confirmation
- After all this main functions will be displayed and user will be asked what he wants to do
    and based on user's choice the corresponding function will be called
        Functions are-
            Withdraw
            Deposit
            Balance Check
            Account Details
            Account Update
            Money Transfer
            PIN Change
            Mini Statement
            Delete This Account
- After every transaction i.e. withdraw, deposit and money transfer , a statement entry will get added in account statements file
- After every update in account detail, it gets updated in acc details file also
        details include-
            - PIN
            - Account Balance (after every transaction)
            - No. of transactions (after every transaction)
            - Mobile No.
            - Age
            - Address


"""

import time
import os

# |-------------------------------------------------| Functions |-------------------------------------------------|

# Create Account
def create_acc():
    i=0
    # while loop is used for convenience like if something invalid happened
    # then instead of exiting the function it'll just execute it from the beginning
    while i < 1:
        # Taking inputs
        with open("list_of_acc.txt") as f:
            xyz = f.read()
        if xyz!="":
            print("Press 0 (zero) to Exit Creating Account")
            f_name = input("First Name: ")
            if f_name == "0":
                break
        else:
            f_name = input("First Name: ")

        l_name = input("Last Name: ")
        if f_name=="" or l_name=="":
            print("Name cannot be empty !")
            continue
        holder_name = f_name.upper() + " " + l_name.upper()

        global const_acc_no

        # Checking for deleted acc no
        with open("deleted_acc_no.txt") as f:
            xyz = f.read()
            f.seek(0)
            deleted_acc_no_lst = f.readlines()

        if xyz=="": # if deleted_acc_no.txt file is empty
            acc_no = const_acc_no + 1 # assigning proper unique account number

        else: # if deleted_acc_no.txt file has some entries
            acc_no = int(str(deleted_acc_no_lst[0])[:11]) # assigning the first entered acc no to the current acc which is being created
            deleted_acc_no_lst.remove(deleted_acc_no_lst[0]) # deleting the acc no which got assigned to the current acc

        # Updating deleted_acc_no.txt with excluded the acc no that got assigned to current acc
        with open("deleted_acc_no.txt", "w") as f:
            for item in deleted_acc_no_lst:
                f.write(item)

        pin = int(input("Create a 4 Digit PIN: "))
        if len(str(pin))!=4: # will check if the PIN contains 4 digits or not
            print("PIN must be of 4 digits\n")
            continue

        re_pin = int(input("Re-enter Your PIN: ")) # confirming PIN
        if re_pin != pin:
            print("PIN didn't match! Please try again..")
            continue
        else:
            print("PIN Matched !")
        print("Creating New Account"
              "\nPlease wait..")

        time.sleep(3)

        print("\nYour Account is Created!")
        print("Account Holder:", holder_name, "\nAccount Number:", acc_no)
        print("\nEnter a few more details:")

        try:
            while True:
                mob_no = int(input("Mobile Number: "))
                if len(str(mob_no))!=10: # will check if the Mobile Number contains 10 digits or not
                    print("Invalid Mobile Number !\nPlease enter valid 10 Digit Mobile Number\n")
                    continue
                else:
                    break

            while True:
                holder_age = int(input("Age: "))
                if holder_age<12: # will check if Age is eligible or not
                    print("Sorry!"
                          "\nYou're Not Eligible"
                          "\nYou must be atleast 12 years old"
                          "\nTry Again..")
                    continue
                elif holder_age>85:
                    print("Sorry!"
                          "\nYou're Not Eligible"
                          "\nYou're too Old to own an Account"
                          "\nTry Again..")
                    continue
                else:
                    break

            male="MALE"
            female="FEMALE"
            while True:
                holder_gender = input("Gender (m/f) : ").upper()
                if holder_gender=="M":
                    holder_gender=male
                    break
                elif holder_gender=="F":
                    holder_gender=female
                    break
                else:
                    print("Invalid Input"
                          "\nPlease try again")
                    continue

            holder_address = input("Address: ").upper()
            if holder_address=="":
                holder_address="-"
            acc_bal = int(input("Please Deposit Some Amount: Rs."))
            trans = 0 # Initiate number of Transactions

        except:
            print("Something went wrong"
                  "\nPlease try again\n")
            continue

        # Create a file for storing transaction history for mini statement
        filename_statement = str(acc_no) + "_statement.txt"
        mini_statement = open(filename_statement, "w")
        content = "Account Number: " + str(acc_no) + \
                  "\nAccount Holder: " + holder_name + \
                  "\nOpening Balance: Rs." + str(acc_bal)+ "\n\n"
        mini_statement.write(content)
        mini_statement.close()

        # Storing Details in accounts dict
        acc_info = {
            "Account Number": acc_no,
            "PIN": pin,
            "Account Balance": acc_bal,
            "Transactions": trans,
            "Mini Statement": filename_statement,
            "Mobile Number": mob_no,
            "Age": holder_age,
            "Gender": holder_gender,
            "Address": holder_address
        }
        accounts_dict[holder_name] = acc_info # Adding Account details in accounts_dict with key as holder_name and value as dict of acc info
        accounts__no_name[acc_no] = holder_name # adding entry in separate dict for linking acc_no with corresponding holder_name

        print("Updating Details"
              "\nPlease wait..")
        time.sleep(2)
        print("Account Details Updated")

        # Create Account Details file
        filename_acc_details = str(acc_no) + ".txt"
        with open(filename_acc_details, "w") as acc_detail:
            content_details = str(acc_no) + "\n" + \
                              holder_name + "\n" + \
                              str(pin) + "\n" + \
                              str(acc_bal) + "\n" + \
                              str(trans)+ "\n"+ \
                              filename_statement+ "\n"+ \
                              str(mob_no)+ "\n" + \
                              str(holder_age)+ "\n"+ \
                              holder_gender+ "\n"+ \
                              holder_address+ "\n"
            acc_detail.write(content_details)

        # Adding entry in list_of_acc.txt file
        with open("list_of_acc.txt", "a") as f:
            content_entry = str(acc_no) + ".txt - " + holder_name+ "\n"
            f.write(content_entry)

        const_acc_no+=1

        # i is incremented so that if program control reaches at this point i.e. after execution of whole function, stop the execution
        # because we've created while loop above
        i += 1

# Update Text File
def update_txt(file, index, new_val):
    """
    This function will take 3 arguments
    1 - filename (without extension)
    2 - index
    3 - new value that will be entered on the place of the value on the specified index

    Working:-
    1.Open the specified file by concatenating <filename> with '.txt'
    2.Store all the content of the file in a list with one line as a single element and by giving proper index. This is our 1st list
    3.Store the element at <index> of 1st list in a separate variable so as to remove it from the list later on
    4.Create a new empty list and using for loop append elements of 1st list into this 2nd list
    5.Insert the <new_val> at <index> of 2nd list and then remove the element that we've stored in step 3
    6.Now we've updated the 2nd list. Using for loop, write each element into the file by opening the file in write mode
    """
    filename = str(file)+ ".txt"

    with open(filename) as f1:
        old_data = f1.readlines()

    old_val = old_data[index]

    updated_data = []
    for item in old_data:
        updated_data.append(item)

    updated_new_val = str(new_val) + "\n"
    updated_data.insert(index,updated_new_val)
    updated_data.remove(old_val)

    with open(filename, "w") as f:
        f.writelines(updated_data)

# Get Date Function
def getdate():
    import datetime
    return datetime.datetime.now()


# |--------------------------------------| Option Functions |-------------------------------------|

"""
Function Parameters:
accounts = dict 'accounts'
acc_name = dict 'Holder Name' in dict 'accounts'
acc_no = Account Number
pin = Current PIN number
bal = Current Balance in Account
trans = Total Transactions of the Account (includes deposits and withdrawals)
mini_statement = filename for mini statement
mob_no = Mobile Number of Holder
age = Age of Holder
gender = Gender of Holder
add = Address of Holder
"""

# 1: Withdraw
def withdraw(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    # while loop is used for convenience like if something invalid happened
    # then instead of exiting the function it'll just execute it from thr beginning
    while True:
        print("\n"
              "Account Holder Name:",acc_name,
              "\nAccount No:",accounts_dict[acc_name][acc_no],
              "\nCurrent Balance: Rs.",accounts_dict[acc_name][bal],
              "\nPress 0 (zero) to Exit Money Withdraw Section")
        try:
            curr_money = int(input("Withdrawal Amount: Rs"))
        except:
            print("Invalid Input")
            continue
        # check if input amount is available in current acc?
        if curr_money > accounts_dict[acc_name][bal]:
            print("Sorry !\nYou don't have enough Balance\n")
            continue
        elif curr_money<0:
            print("Unacceptable Input")
            continue
        elif curr_money==0:
            break
        print("Transaction in Process..."
              "\nPlease wait..")

        accounts_dict[acc_name][bal] -= curr_money # subtract the withdrawal amt from the balance
        accounts_dict[acc_name][trans] +=1 # increment Number of Transactions of the Acc

        # Add Entry in the Statement of Account
        statement = open(accounts_dict[acc_name][mini_statement], "a")
        entry = f"[ {str(getdate())} ]: (  - ) {str(curr_money)}/-\nClosing Balance: Rs.{accounts_dict[acc_name][bal]}\n\n"
        statement.write(entry)
        statement.close()

        update_txt(accounts_dict[acc_name][acc_no],3,accounts_dict[acc_name][bal]) # update account_balance in txt file of the Account
        update_txt(accounts_dict[acc_name][acc_no],4,accounts_dict[acc_name][trans]) # update number_of_transactions in txt file of the Account
        time.sleep(5)
        print(f"\nWithdrawal Success!\nLeft Balance: Rs.{accounts_dict[acc_name][bal]}")
        break

# 2: Deposit
def deposit(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    while True:
        print("\n"
              "Account Holder Name:", acc_name,
              "\nAccount No:", accounts_dict[acc_name][acc_no],
              "\nCurrent Balance: Rs.", accounts_dict[acc_name][bal],
              "\nPress 0 (zero) to Exit Money Deposit Section")
        try:
            curr_money = int(input("Deposit Amount: Rs"))
        except:
            print("Invalid Input")
            continue
        if curr_money<0:
            print("Unacceptable Input")
            continue
        elif curr_money==0:
            break
        print("Transaction in Process..."
              "\nPlease wait..")

        accounts_dict[acc_name][bal] += curr_money # add the deposit amt to the balance
        accounts_dict[acc_name][trans] +=1 # increment Number of Transactions of the Acc

        statement = open(accounts_dict[acc_name][mini_statement], "a")
        entry = f"[ {str(getdate())} ]: ( + ) {str(curr_money)}/-\nClosing Balance: Rs.{accounts_dict[acc_name][bal]}\n\n"
        statement.write(entry)
        statement.close()

        update_txt(accounts_dict[acc_name][acc_no],3,accounts_dict[acc_name][bal]) # update account_balance in txt file of the Account
        update_txt(accounts_dict[acc_name][acc_no],4,accounts_dict[acc_name][trans]) # update number_of_transactions in txt file of the Account
        time.sleep(5)
        print("\nDeposit Success!\nNew Balance: Rs.", accounts_dict[acc_name][bal])
        break

# 3: Balance Check
def bal_check(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    print("Account Holder Name:",acc_name,
          "\nAccount Number:",accounts_dict[acc_name][acc_no],
          "\nCurrent Balance: Rs.",accounts_dict[acc_name][bal],
          "\nTotal Transactions Done:",accounts_dict[acc_name][trans])

# 4: Account Details
def acc_details(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    print("Account Number:",accounts_dict[acc_name][acc_no],
          "\nAccount Holder:",acc_name,
          "\nCurrent Balance: Rs.",accounts_dict[acc_name][bal],
          "\nTotal Transactions Done:",accounts_dict[acc_name][trans],
          "\nMobile Number:",accounts_dict[acc_name][mob_no],
          "\nAge:",accounts_dict[acc_name][age],
          "\nGender:",accounts_dict[acc_name][gender],
          "\nAddress:",accounts_dict[acc_name][add]
          )

# 5: Account Update
def acc_update(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    print("Account Update Section")
    print("Your Current Account Details:"
          "\nAccount Holder Name: ",acc_name,
          "\nAccount Number: ",accounts_dict[acc_name][acc_no],
          "\nMobile Number: ",accounts_dict[acc_name][mob_no],
          "\nAge: ",accounts_dict[acc_name][age],
          "\nAddress: ",accounts_dict[acc_name][add])

    # while loop is used for convenience like if something invalid happened
    # then instead of exiting the function it'll just execute it from thr beginning
    while True:
        print("\n\nSelect Detail you want to change:"
              "\n1 - Mobile Number"
              "\n2 - Age (Do this only once a Year)"
              "\n3 - Address"
              "\nPress 0 (zero) to Exit Account Update Section")
        op = int(input("Your Choice: ")) # choose option (1,2,3)
        if op == 0:
            break

        # <index_for_details_update> variable will specify the proper index for update_txt() function
        elif op==1:
            index_for_details_update = 6
            print("Current Mobile Number:", accounts_dict[acc_name][mob_no],"\n")
            try:
                new = int(input("New Mobile Number: "))
            except:
                print("Invalid Input ")
                continue
            if len(str(new))!=10:
                print("Invalid Mobile Number"
                      "\nPlease enter a Valid 10 Digit Mobile Number")
                continue
            accounts_dict[acc_name][mob_no] = new
            print("Mobile Number Updated Successfully!"
                  "\nUpdated Mobile Number:", accounts_dict[acc_name][mob_no])

        elif op==2:
            index_for_details_update = 7
            print("Current Age:",accounts_dict[acc_name][age])
            accounts_dict[acc_name][age] +=1
            new = accounts_dict[acc_name][age]
            print("Age Updated Successfully!"
                  "\nUpdated Age:", accounts_dict[acc_name][age])

        elif op==3:
            index_for_details_update = 9
            print("Current Address:",accounts_dict[acc_name][add])
            new = input("New Address: ").upper()
            if new=="" or new==" ":
                new="-"
            accounts_dict[acc_name][add] = new
            print("Address Updated Successfully!"
                  "\nUpdated Address:", accounts_dict[acc_name][add])

        else:
            print("Invalid Choice")
            continue

        update_txt(accounts_dict[acc_name][acc_no], index_for_details_update, new)

        # Ask user if he/she wants to update any other field?
        answer_raw = input("Do you want to change any other field? (y/n): ")
        answer = answer_raw.upper()
        if answer=="Y":
            continue
        elif answer=="N":
            break
        else:
            print("Invalid Input\nExiting the Options...")
            break

# 6: Money Transfer
def money_transfer(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    # while loop is used for convenience like if something invalid happened
    # then instead of exiting the function it'll just execute it from thr beginning
    while True:
        print("\nMoney Transfer Section:")

        # Display Accounts to transfer money to for user to choose
        print("List of Accounts:")
        for item in accounts_dict:
            # will not display current account
            if item != accounts__no_name[accounts_dict[acc_name][acc_no]]:
                print(f"- {accounts_dict[item][acc_no]} - {item}")

        print("Press 0 (zero) to Exit Money Transfer Section")
        try:
            to_acc = int(input("\nTo Account ( Just Enter last 4 digits of Account Number ) : "))
        except:
            print("Invalid Choice")
            continue
        if to_acc==0:
            break

        to_acc += 42298010000 # will return a proper acc_no

        # check if acc_no is valid or not?
        if to_acc not in accounts__no_name:
            print("Account Number doesn't exist\nPlease Enter Valid Input")
            continue
        # if user entered current account's no
        elif to_acc==accounts_dict[acc_name][acc_no]:
            print("Sorry !"
                  "\nIt seems like you are trying to transfer money to your own Account which cannot be done"
                  "\nPlease choose another Account")
            continue

        print(f"\nAccount Selected : {accounts__no_name[to_acc]}")
        print(f"Current Balance in your Account - Rs.{accounts_dict[acc_name][bal]}")
        try:
            amt = int(input("Enter Amount to Transfer: Rs."))
        except:
            print("Invalid Input")
            continue
        # check if input amount is available in current acc?
        if amt>accounts_dict[acc_name][bal]:
            print("Sorry !\nYou don't have enough Balance\n")
            continue
        if amt<=0:
            print("Unacceptable Input")
            continue

        print("Transaction in Process..")
        accounts_dict[acc_name][trans] +=1 # increment Number of Transactions of the transfer_from_account
        accounts_dict[accounts__no_name[to_acc]][trans] +=1 # increment Number of Transactions of the transfer_to_account

        accounts_dict[acc_name][bal] -= amt # will subtract input_amt from balance of from_account
        accounts_dict[accounts__no_name[to_acc]][bal] += amt # will add input_amt to balance of to_account
        current_time = getdate() # take record of time of transaction

        update_txt(accounts_dict[acc_name][acc_no],3,accounts_dict[acc_name][bal]) # will update account balance in txt file of transfer_from_account
        update_txt(to_acc,3,accounts_dict[accounts__no_name[to_acc]][bal]) # will update account balance in txt file of transfer_to_account

        update_txt(accounts_dict[acc_name][acc_no],4,accounts_dict[acc_name][trans]) # update number_of_transactions in txt file of transfer_from_account
        update_txt(to_acc,4,accounts_dict[accounts__no_name[to_acc]][trans]) # will update account balance in txt file of transfer_to_account


        # Mini Statement entry in from_account file
        with open(f"{accounts_dict[acc_name][acc_no]}_statement.txt", "a") as f:
            entry = f"[ {str(current_time)} ]: ( - ) {amt}/- \t\t " \
                    f"Sent to Account No - {to_acc} ({accounts__no_name[to_acc]})" \
                    f"\nClosing Balance: Rs.{accounts_dict[acc_name][bal]}\n\n"
            f.write(entry)

        # Mini Statement entry in to_account file
        with open(f"{to_acc}_statement.txt", "a") as f:
            entry = f"[ {str(current_time)} ]: ( + ) {amt}/- \t\t " \
                    f"Received from Account No - {accounts_dict[acc_name][acc_no]} ({acc_name})" \
                    f"\nClosing Balance: Rs.{accounts_dict[accounts__no_name[to_acc]][bal]}\n\n"
            f.write(entry)

        time.sleep(5)

        print(f"\nMoney Transfered Successfully to Account Number: {to_acc} - {accounts__no_name[to_acc]}"
              f"\nBalance Left in Current Account - Rs.{accounts_dict[acc_name][bal]}")
        break


# 7: Pin Change
def pin_change(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    # while loop is used for convenience like if something invalid happened
    # then instead of exiting the function it'll just execute it from thr beginning
    while True:
        print("\nCurrent Account:"
              "\nAccount Holder:",acc_name,
              "\nAccount Number:",accounts_dict[acc_name][acc_no],
              "\nPress 0 (zero) toExit PIN Change Section")
        try:
            re_pin = int(input("Confirm Your Current PIN: "))
        except:
            print("Invalid Input")
            continue
        if re_pin==0:
            break
        # confirm current PIN
        elif re_pin==accounts_dict[acc_name][pin]:
            try:
                new_pin = int(input("New PIN: "))
            except:
                print("Invalid Input")
                continue
            if len(str(new_pin))!=4:
                print("PIN must be of 4 digits\n")
                continue
            elif new_pin==accounts_dict[acc_name][pin]:
                print("It seems like you entered same PIN"
                      "\nPlease enter a new PIN")
                continue
            try:
                renew_pin = int(input("Re-enter New PIN: "))
            except:
                print("Invalid Input")
                continue
            # confirm new PIN
            if renew_pin==new_pin:
                accounts_dict[acc_name][pin] = new_pin
                update_txt(accounts_dict[acc_name][acc_no],2,accounts_dict[acc_name][pin]) # update PIN in acc_details file
                print("PIN Changed Successfully")
                break
            else:
                print("Please Enter same New PIN")
                continue

        else:
            print("Wrong PIN\n")
            continue

# 8: Mini Statement
def mini_statement(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    with open(accounts_dict[acc_name][mini_statement]) as f:
        print(f.read())

# 9: Delete Account
def del_acc(accounts_dict, acc_name, acc_no, pin, bal, trans, mini_statement, mob_no, age, gender, add):
    while True:
        print("Press 0 (zero) to Exit Delete Account Section")
        try:
            re_pin=int(input("Confirm your PIN: "))
        except:
            print("Invalid Input")
            continue
        if re_pin==0: # if user inputs zero it'll exit the function using 'break'
            break
        elif re_pin==accounts_dict[acc_name][pin]:
            print("PIN Matched !"
                  "\nDeleting Your Account"
                  "\nPlease wait..")
            global const_acc_no
            const_acc_no -= 1 # decrementing const_acc_no so as to make it proper if use creates another account at same runtime

            # Deleting account files
            acc_details_file = f"{str(accounts_dict[acc_name][acc_no])}.txt"
            acc_statement_file = f"{str(accounts_dict[acc_name][acc_no])}_statement.txt"
            os.remove(acc_details_file)
            os.remove(acc_statement_file)

            # Deleting entry from list_of_acc.txt file
            with open("list_of_acc.txt") as f:
                content_lst = f.readlines()

            item = f"{str(accounts_dict[acc_name][acc_no])}.txt - {accounts__no_name[accounts_dict[acc_name][acc_no]]}\n"
            content_lst.remove(item)

            with open("list_of_acc.txt", "w") as f:
                for item in content_lst:
                    f.write(item)

            # Adding Current Account's No in deleted_acc_no.txt file
            with open("deleted_acc_no.txt", "a") as f:
                del_acc_entry = f"{str(accounts_dict[acc_name][acc_no])}\n"
                f.write(del_acc_entry)

            # Deleting Account from dicts
            del accounts__no_name[accounts_dict[acc_name][acc_no]]
            del accounts_dict[acc_name]

            time.sleep(3)
            print("Your Account has been Deleted Successfully !")
            break

        else: # if user entered wrong PIN
            print('Wrong PIN'
                  '\nPlease try again..')
            continue

# |-------------------------------------------------| Welcome Statement |-------------------------------------------------|
print("Welcome to Python Banking"
      "\nInitializing")
# Main Accounts dict
accounts_dict = {}
# Separate dict for linking acc_no with respective holder_name
accounts__no_name = {}
const_acc_no = 42298012500

# |-------------------------------------------------| Checking for existing accounts |-------------------------------------------------|
print("Checking for Exisiting Accounts.."
      "\nPlease wait....")

list_of_acc_file = open("list_of_acc.txt", "a")  # will create the file to store list of accounts if the program is running for the first time
list_of_acc_file.close()

deleted_acc_no_file = open("deleted_acc_no.txt", "a")  # will create the file to store list of deleted account numbers if the program is running for the first time
deleted_acc_no_file.close()

with open("list_of_acc.txt") as list_of_acc: # list_of_acc.txt file opened
    xyz = list_of_acc.read()
    time.sleep(5)
    # check if there is any existing account or not
    if xyz=="":
        print("\nOops !"
              "\nNo existing Account found in the Database"
              "\nCreate Account first\n")
        create_acc() # Since no existing accounts found, it'll ask user to create account
    else:
        list_of_acc.seek(0) # to seek the cursor to the starting of the file
        acc_lst_raw = list_of_acc.readlines() # store all entries from list_of_acc.txt in a list

        acc_lst_processed = [] # to store actual filenames from acc_lst_raw
        for item_in_lst in acc_lst_raw:
            acc_lst_processed.append(item_in_lst[:15]) # will exclude useless string
            const_acc_no+=1 # to increment const_acc_no for each existing account entry so that when we create new account it'll get the updated account no

        for item_in_acc_lst in acc_lst_processed:
            try:
                with open(item_in_acc_lst) as f:
                    pass
            except:
                continue
            with open(item_in_acc_lst) as Account: # Account file opened
                details_raw = Account.readlines() # will store details in a list - details_raw with '\n'

            details_processed = [] # to store details excluding '\n'
                # to remove '\n'
            for item_in_details_raw in details_raw:
                index = len(item_in_details_raw) - 1
                details_processed.append(item_in_details_raw[:index])

            # Storing details separately
            acc_no = int(details_processed[0])                               # Account Number
            acc_holder_name = details_processed[1]                    # Holder Name
            acc_pin = int(details_processed[2])                              # PIN
            acc_bal = int(details_processed[3])                              # Account Balance
            acc_trans = int(details_processed[4])                          # Total Transactions
            acc_mini_statement = details_processed[5]                # Mini Statement
            acc_holder_mob = int(details_processed[6])               # Mobile Number
            acc_holder_age= int(details_processed[7])                 # Age
            acc_holder_gender = details_processed[8]                # Gender
            acc_holder_add = details_processed[9]                     # Address

            # Storing details in dict
            acc_info = {
                "Account Number": acc_no,
                "PIN": acc_pin,
                "Account Balance": acc_bal,
                "Transactions": acc_trans,
                "Mini Statement": acc_mini_statement,
                "Mobile Number": acc_holder_mob,
                "Age": acc_holder_age,
                "Gender": acc_holder_gender,
                "Address": acc_holder_add
            }

            # Adding Account into accounts_dict
            accounts_dict[acc_holder_name] = acc_info
            # linking acc_no with respective acc_holder_name
            accounts__no_name[acc_no] = acc_holder_name

        print("\nExisting Accounts Found:")
        # Below code is just for trial
        # for name in accounts_dict:
        # print(name)
        # print(accounts_dict)

# |-------------------------------------------------| BANKING |-------------------------------------------------|
while True: # For repeated banking

    #  |-------------------------------------------------| Selecting Account |-------------------------------------------------|

    print("\nSelect Your Account:")

    # Display list of all Accounts
    for name in accounts_dict:
        print("- ", accounts_dict[name]["Account Number"], " - ",name)
    print("Or Press 1 to Create New Account\n")
    try:
        select_acc = int(input("Enter last 4 digits of your Account Number from the given list: "))
    except:
        print("Invalid Input"
              "\nTry again")
        continue

    if select_acc ==1:
        create_acc()
        continue
    else:
        try:
            select_acc += 42298010000  # will return a proper acc_no
            choose_acc = accounts__no_name[select_acc]
            # checking the PIN
            re_pin = int(input("Enter 4 Digit PIN: "))
            if re_pin!=accounts_dict[choose_acc]["PIN"]:
                print("Incorrect PIN\nPlease try again.\n")
                continue
            else:
                print("Correct PIN!")
            print("\nAccount Selected: ", choose_acc)
        except:
            print("Please Select Valid Account!")
            continue

    #  |-------------------------------------------------| Choosing Options |-------------------------------------------------|
    while True:
        print("\nChoose Option\n"
              "Press The Corresponding Number to Choose\n"
              "1 - Withdraw\n"
              "2 - Deposit\n"
              "3 - Balance Check\n"
              "4 - Account Details\n"
              "5 - Account Update\n"
              "6 - Money Transfer\n"
              "7 - Change PIN\n"
              "8 - Mini Statement\n"
              "9 - Delete This Account\n")
        try:
            choose_op = int(input("Option - "))
        except:
            print("Invalid Input")
            continue
        if choose_op<1 or choose_op>9:
            print("Choose Valid Option\n")
            continue
        else:
            print("")
            break

    #  |-------------------------------------------------| Switch Between Options |-------------------------------------------------|

    # dict is created for switching between options
    options = {
        1: withdraw,
        2: deposit,
        3: bal_check,
        4: acc_details,
        5: acc_update,
        6: money_transfer,
        7: pin_change,
        8: mini_statement,
        9: del_acc
    }

    # options.get() will return the value of corresponding choose_op i.e. name_of_function
    # after that arguments are passed for the function in parenthesis
    options.get(choose_op)(accounts_dict,choose_acc,"Account Number","PIN","Account Balance","Transactions","Mini Statement","Mobile Number","Age","Gender","Address")

    #  |-------------------------------------------------| Ask User to Continue or Not |-------------------------------------------------|

    ans = input("\nDo you want to continue Banking? (y/n) - ").upper()
    if ans=="N":
        print("\nThank You For Using Our Program !")
        break
    elif ans=="Y":
        print("\nIt Seems Like You Are Enjoying Our Program.\n")
        continue
    else:
        print("Invalid Choice"
              "\nQuitting the Program")
        break
