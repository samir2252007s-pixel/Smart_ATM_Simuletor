import json
import os

DATA_FILE = "atm_data.json"

# بيانات افتراضية في حال عدم وجود ملف سابق
default_accounts = {
    "1001": {
        "pin": "1234",
        "name": "Mohamed",
        "balance": 5000,
        "transactions": []
    },
    "1002": {
        "pin": "5678",
        "name": "Samir",
        "balance": 7000,
        "transactions": []
    },
    "1003": {
        "pin": "9999",
        "name": "Ahmed",
        "balance": 3000,
        "transactions": []
    }
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return default_accounts

def save_data(accounts):
    with open(DATA_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

accounts = load_data()

def authenticate_account():
    attempts = 0
    while attempts < 3:
        account_number = input("Enter account number: ")
        pin = input("Enter PIN: ")

        if account_number in accounts:
            if accounts[account_number]["pin"] == pin:
                print(f"Login Successful! Welcome, {accounts[account_number]['name']}")
                return account_number

        attempts += 1
        print("Invalid account number or PIN")

    print("Maximum attempts reached")
    return None

def show_menu():
    print("\n========== SMART ATM ==========")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Change PIN")
    print("6. Transaction Summary")
    print("7. Logout")
    print("===============================")

def check_balance(account_number):
    balance = accounts[account_number]["balance"]
    print(f"Current Balance = {balance}")

def deposit(account_number, amount):
    if amount <= 0:
        print("Invalid deposit amount")
        return

    accounts[account_number]["balance"] += amount
    accounts[account_number]["transactions"].append(f"Deposited {amount}")
    save_data(accounts)
    print("Deposit Successful")

def withdraw(account_number, amount):
    if amount <= 0:
        print("Invalid withdrawal amount")
        return

    if amount > accounts[account_number]["balance"]:
        print("Insufficient Balance")
        return

    accounts[account_number]["balance"] -= amount
    accounts[account_number]["transactions"].append(f"Withdrew {amount}")
    save_data(accounts)
    print("Withdrawal Successful")

def transfer_money(from_account, to_account, amount):
    if to_account not in accounts:
        print("Destination Account Not Found")
        return

    if to_account == from_account:
        print("Cannot transfer to the same account")
        return

    if amount <= 0:
        print("Invalid transfer amount")
        return

    if amount > accounts[from_account]["balance"]:
        print("Insufficient Balance")
        return

    accounts[from_account]["balance"] -= amount
    accounts[to_account]["balance"] += amount
    
    accounts[from_account]["transactions"].append(f"Transferred {amount} to {to_account}")
    accounts[to_account]["transactions"].append(f"Received {amount} from {from_account}")
    
    save_data(accounts)
    print("Transfer Successful")

def change_pin(account_number):
    old_pin = input("Enter current PIN: ")
    if old_pin == accounts[account_number]["pin"]:
        new_pin = input("Enter new PIN (4 digits): ")
        if len(new_pin) == 4 and new_pin.isdigit():
            accounts[account_number]["pin"] = new_pin
            save_data(accounts)
            print("PIN Changed Successfully")
        else:
            print("Invalid PIN format. Must be 4 digits.")
    else:
        print("Incorrect current PIN")

def transaction_summary(account_number):
    print("\n--- Transaction Summary ---")
    trans = accounts[account_number]["transactions"]
    if not trans:
        print("No transactions yet.")
    else:
        for t in trans:
            print(f"- {t}")

def main():
    current_account = authenticate_account()
    if current_account:
        while True:
            show_menu()
            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                check_balance(current_account)
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to deposit: "))
                    deposit(current_account, amount)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '3':
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    withdraw(current_account, amount)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '4':
                to_account = input("Enter destination account number: ")
                try:
                    amount = float(input("Enter amount to transfer: "))
                    transfer_money(current_account, to_account, amount)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
                change_pin(current_account)
            elif choice == '6':
                transaction_summary(current_account)
            elif choice == '7':
                print("Logging out. Thank you for using Smart ATM!")
                break
            else:
                print("Invalid choice, please select from 1 to 7.")
                
            input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    main()
