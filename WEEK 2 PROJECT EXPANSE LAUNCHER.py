"""WEEK 2 PROJECT """
# Expanse Launcher
#Decode lab internship 
#Project WEEK 2


import os
from datetime import datetime

EXIT_COMMANDS = ["quit", "exit", "q"]
LOG_FILE = "expense_history.txt"


def is_exit_command(user_input):
    return user_input.lower() in EXIT_COMMANDS


def convert_to_number(user_input):
    try:
        amount = float(user_input)
        if amount >= 0:
            return amount
    except ValueError:
        pass
    return None


def get_category():
    categories = ["Food", "Travel", "Bills", "Shopping", "Other"]

    print("\nCategories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    choice = input("Choose category number (Press Enter for Other): ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(categories):
        return categories[int(choice) - 1]

    return "Other"


def add_expense(expenses, amount, category):
    expense = {
        "amount": amount,
        "category": category,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    expenses.append(expense)


def remove_last_expense(expenses):
    if not expenses:
        print("\nNothing to undo.")
        return

    removed = expenses.pop()
    print(f"\nRemoved: {removed['category']} - {removed['amount']:.2f}")


def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total


def category_totals(expenses):
    totals = {}

    for expense in expenses:
        category = expense["category"]

        if category not in totals:
            totals[category] = 0

        totals[category] += expense["amount"]

    return totals


def highest_expense(expenses):
    if not expenses:
        return None
    return max(expenses, key=lambda x: x["amount"])


def lowest_expense(expenses):
    if not expenses:
        return None
    return min(expenses, key=lambda x: x["amount"])


def show_history(expenses):
    if not expenses:
        print("\nNo expenses added yet.")
        return

    print("\nExpense History")
    print("-" * 55)

    for i, expense in enumerate(expenses, start=1):
        print(
            f"{i}. {expense['category']} | "
            f"{expense['amount']:.2f} | "
            f"{expense['time']}"
        )

    print()


def save_to_file(expenses, total):
    with open(LOG_FILE, "w") as file:
        file.write("EXPENSE TRACKER REPORT\n")
        file.write(f"Generated: {datetime.now()}\n")
        file.write("=" * 50 + "\n")

        for i, expense in enumerate(expenses, start=1):
            file.write(
                f"{i}. {expense['category']} - "
                f"{expense['amount']:.2f} - "
                f"{expense['time']}\n"
            )

        file.write("=" * 50 + "\n")
        file.write(f"TOTAL SPENT: {total:.2f}")

    print("\nReport saved successfully.")
    print(os.path.abspath(LOG_FILE))


def show_menu():
    print("\n========== Expense Tracker ==========")
    print("Enter an amount to add an expense.")
    print("Commands:")
    print("history   undo   stats   save   quit")
    print("=" * 35)


def show_stats(expenses):
    if not expenses:
        print("\nNo data available.")
        return

    total = calculate_total(expenses)
    average = total / len(expenses)

    highest = highest_expense(expenses)
    lowest = lowest_expense(expenses)

    totals = category_totals(expenses)

    print("\n------ Statistics ------")
    print(f"Transactions : {len(expenses)}")
    print(f"Total Spent  : {total:.2f}")
    print(f"Average      : {average:.2f}")
    print(f"Highest      : {highest['category']} - {highest['amount']:.2f}")
    print(f"Lowest       : {lowest['category']} - {lowest['amount']:.2f}")

    print("\nCategory Totals")
    for category, amount in totals.items():
        print(f"{category}: {amount:.2f}")


def run_tracker():
    expenses = []

    show_menu()

    while True:
        user_input = input("\nEnter amount or command: ").strip()

        if not user_input:
            continue

        if is_exit_command(user_input):
            break

        command = user_input.lower()

        if command == "history":
            show_history(expenses)
            continue

        if command == "undo":
            remove_last_expense(expenses)
            continue

        if command == "stats":
            show_stats(expenses)
            continue

        if command == "save":
            save_to_file(expenses, calculate_total(expenses))
            continue

        amount = convert_to_number(user_input)

        if amount is None:
            print("Please enter a valid positive amount.")
            continue

        category = get_category()

        add_expense(expenses, amount, category)

        total = calculate_total(expenses)

        print(f"\nAdded {category} expense of {amount:.2f}")
        print(f"Running Total: {total:.2f}")

    final_total = calculate_total(expenses)

    print("\nFinal Summary")
    show_history(expenses)
    show_stats(expenses)

    save = input("\nDo you want to save the report? (y/n): ").strip().lower()

    if save == "y":
        save_to_file(expenses, final_total)

    print(f"\nFinal Total Spent: {final_total:.2f}")
    print("Thank you for using Expense Tracker!")


if __name__ == "__main__":
    run_tracker()