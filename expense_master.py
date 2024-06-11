import pandas as pd
import re
from datetime import datetime

def action():
    action_option = input(
        "Do you want to add, edit, delete or view your expenses? ").lower()
    if action_option == 'add':
        add_expense()
    elif action_option == 'edit':
        edit_expense()
    elif action_option == 'view':
        view_expense()
    elif action_option == 'delete':
        delete_expense()
    else:
        print("Invalid option")


def add_expense():
    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_amount(amount_str):
        try:
            float(amount_str)
            return True
        except ValueError:
            return False

    def is_text(input_str):
        return bool(re.match(r'^[a-zA-Z\s]+$', input_str))

    def is_non_empty_string(input_str):
        return bool(input_str.strip())

    def get_valid_input(prompt, validation_func, error_message):
        while True:
            user_input = input(prompt)
            if validation_func(user_input):
                return user_input
            else:
                print(error_message)

    date = get_valid_input("Enter date (YYYY-MM-DD): ", is_valid_date,
                            "Invalid date. Please enter a date in the format YYYY-MM-DD.")
    amount = get_valid_input("Enter price amount: ", is_valid_amount,
                                "Invalid amount. Please enter a valid number.")
    category = get_valid_input("Enter category: ", is_text,
                                "Invalid category. Please enter a valid text.")
    description = get_valid_input("Enter description: ", is_text,
                                    "Invalid description. Please enter a valid text.")

    data = {
        'Date': [date],
        'Amount': [float(amount)],  # Converting amount to float
        'Category': [category],
        'Description': [description],
    }

    try:
        df = pd.read_csv('data.csv')
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(data)

    df.to_csv('data.csv', index=False)
    print("Expense added successfully.")



def edit_expense():
    try:
        df = pd.read_csv('data.csv')
        print("Current Expenses:")
        print(df)

        index = int(input("Enter the index of the expense you want to edit: "))
        if index in df.index:
            date = input(
                "Enter new date (YYYY-MM-DD) or press Enter to skip: ")
            amount = input("Enter new price amount or press Enter to skip: ")
            category = input("Enter new category or press Enter to skip: ")
            description = input(
                "Enter new description or press Enter to skip: ")

            if date:
                df.at[index, 'Date'] = date
            if amount:
                df.at[index, 'Amount'] = amount
            if category:
                df.at[index, 'Category'] = category
            if description:
                df.at[index, 'Description'] = description

            df.to_csv('data.csv', index=False)
            print("Expense updated successfully.")
        else:
            print("Invalid index.")
    except FileNotFoundError:
        print("No expense records found.")
    except ValueError:
        print("Invalid input for index.")


def view_expense():
    try:
        df = pd.read_csv('data.csv')
        print("Current Expenses:")
        print(df)
    except FileNotFoundError:
        print("No expense records found.")

def delete_expense():
    try:
        df = pd.read_csv('data.csv')
        print("Current Expenses:")
        print(df)

        index = int(input("Enter the index of the expense you want to delete: "))
        if index in df.index:
            df.drop(index, inplace=True)
            df.to_csv('data.csv', index=False)
            print("Expense deleted successfully.")
        else:
            print("Invalid index.")
    except FileNotFoundError:
        print("No expense records found.")
    except ValueError:
        print("Invalid input for index.")


if __name__ == '__main__':
    action()
