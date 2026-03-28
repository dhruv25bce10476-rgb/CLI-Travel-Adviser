# main.py
from auth import login, signup
from traveladviser import run_travel_planner

BANNER = """
  ╔══════════════════════════════════════════════════╗
  ║         DW TRAVEL ADVISER  —  v2.0              ║
  ║         ✈  Plan smarter. Travel better.         ║
  ╚══════════════════════════════════════════════════╝
"""

def main():
    print(BANNER)
##This loop works while true, allows for Login, SignUp and Exiting the application
    while True:
        print("  [1]  Login")
        print("  [2]  Sign Up")
        print("  [3]  Exit")
        print()

        choice = input("  Select option: ").strip()

        if choice == "1":
            user = login()
            if user:
                print(f"\n  Welcome, {user['first_name']} {user['last_name']}! 👋")
                run_travel_planner()

        elif choice == "2":
            signup()

        elif choice == "3":
            print("\n  Thank you for using DW Travel Adviser. Goodbye! 👋\n")
            break

        else:
            print("  Invalid choice. Enter 1, 2 or 3.\n")

if __name__ == "__main__":
    main()
