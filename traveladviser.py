# traveladviser.py
import pandas as pd
import os
from flight_rates import display_flight_options, get_flight_options

CSV_FILE = "Travel_list.csv"

def load_data():
    path = os.path.join(os.path.dirname(__file__), CSV_FILE)
    return pd.read_csv(path)

def divider(char="─", width=50):
    print("  " + char * width)

def print_header(title):
    print()
    divider()
    print(f"  {title}")
    divider()

# ─── PLAN A TRIP ──────────────────────────────────────────────────────────────

def plan_trip(df):
    while True:
        print_header("DESTINATIONS")
        for i, row in df.iterrows():
            print(f"  [{i+1:>2}]  {row['Country']:<16}  Safety: {row['Safety Rating (1-10)']}/10  |  {row['Known For']}")
        print()
        print("  [0]  Back to menu")
        divider()

        try:
            choice = int(input("  Select a country: "))
        except ValueError:
            print("  Enter a valid number.")
            continue

        if choice == 0:
            return
        if choice < 1 or choice > len(df):
            print("  Invalid choice.")
            continue

        country = df.iloc[choice - 1]
        country_name = country["Country"]

        print(f"\n  ─── {country_name.upper()} ──────────────────────────────────")
        print(f"  Known for   : {country['Known For']}")
        print(f"  Best time   : {country['Best Time to Visit']}")
        print(f"  Currency    : {country['Currency']}  (1 {country['Currency']} = ₹{country['Currency Rate (1 unit to INR)']})")
        print(f"  Safety      : {country['Safety Rating (1-10)']}/10")

        # Flight options
        flight_price = display_flight_options(country_name)

        # Persons, rooms & nights
        print()
        try:
            persons = int(input("  Number of persons      : "))
            rooms   = int(input("  Number of rooms        : "))
            nights  = int(input("  Number of nights       : "))
            if persons < 1 or rooms < 1 or nights < 1:
                raise ValueError
        except ValueError:
            print("  Invalid input. Returning to list.")
            continue

        # Cost breakdown
        hotel = country["Avg Hotel per Night (INR)"]
        misc  = country["Misc Expenses per Day (INR)"]
        visa  = country["Visa Cost (INR)"]

        flight_total = flight_price * persons   # flight is per person
        hotel_total  = hotel * rooms * nights   # hotel is per room per night
        misc_total   = misc  * persons * nights # misc is per person per day
        visa_total   = visa  * persons          # visa is per person
        grand_total  = flight_total + hotel_total + misc_total + visa_total
        per_person   = round(grand_total / persons)

        print()
        divider("═")
        print(f"  COST BREAKDOWN — {country_name.upper()}")
        divider("═")
        print(f"  ✈  Flight      ₹{flight_price:>8,}  × {persons} person(s)  = ₹{flight_total:>10,}")
        print(f"  🏨  Hotel       ₹{hotel:>8,}  × {rooms} room(s) × {nights}n = ₹{hotel_total:>10,}")
        print(f"  🎒  Misc        ₹{misc:>8,}  × {persons} person(s) × {nights}n = ₹{misc_total:>10,}")
        print(f"  📄  Visa        ₹{visa:>8,}  × {persons} person(s)  = ₹{visa_total:>10,}")
        divider()
        print(f"  💰  TOTAL COST                           ₹{grand_total:>10,}")
        print(f"  👤  Per person                           ₹{per_person:>10,}")
        divider("═")

        # Budget rating
        if grand_total < 200000:
            print("  💸  Budget tier : BUDGET FRIENDLY ✓")
        elif grand_total < 500000:
            print("  💸  Budget tier : MID-RANGE")
        else:
            print("  💸  Budget tier : PREMIUM")

        # Safety advisory
        safety = country["Safety Rating (1-10)"]
        if safety >= 9:
            print(f"  🛡  Safety      : Excellent ({safety}/10) — very safe to travel.")
        elif safety >= 7:
            print(f"  🛡  Safety      : Good ({safety}/10) — generally safe, stay alert.")
        else:
            print(f"  🛡  Safety      : Caution ({safety}/10) — check travel advisories before going.")

        print()
        again = input("  Plan another trip? (yes / no): ").strip().lower()
        if again != "yes":
            return


# ─── SMART RECOMMEND ─────────────────────────────────────────────────────────

def smart_recommend(df):
    print_header("SMART RECOMMENDER")
    print("  We'll suggest the best destinations based on your budget.")
    print()

    try:
        budget  = int(input("  Total budget (₹)        : ").replace(",", ""))
        persons = int(input("  Number of persons        : "))
        nights  = int(input("  Number of nights         : "))
        if budget < 1 or persons < 1 or nights < 1:
            raise ValueError
    except ValueError:
        print("  Invalid input.")
        input("  Press Enter to continue...")
        return

    print("\n  Searching destinations...\n")

    results = []
    for _, row in df.iterrows():
        country = row["Country"]
        options = get_flight_options(country)
        flight  = options["Economy"]          # use economy for recommendation

        hotel = row["Avg Hotel per Night (INR)"]
        misc  = row["Misc Expenses per Day (INR)"]
        visa  = row["Visa Cost (INR)"]

        total    = flight * persons + hotel * persons * nights + misc * persons * nights + visa * persons
        per_p    = round(total / persons)
        leftover = budget - total

        if total <= budget:
            results.append({
                "country":  country,
                "known_for": row["Known For"],
                "best_time": row["Best Time to Visit"],
                "safety":   row["Safety Rating (1-10)"],
                "total":    total,
                "per_p":    per_p,
                "leftover": leftover,
                "flight":   flight,
                "currency": row["Currency"],
            })

    if not results:
        print("  ✗ No destinations found within your budget.")
        print("  Tip: Try increasing your budget or reducing nights.")
        input("\n  Press Enter to continue...")
        return

    # Sort: safety desc, then cost asc
    results.sort(key=lambda x: (-x["safety"], x["total"]))

    print(f"  ✓ Found {len(results)} destination(s) within ₹{budget:,}:\n")
    divider("═")

    for rank, r in enumerate(results[:5], 1):
        badge = "★ TOP PICK" if rank == 1 else f"#{rank}"
        print(f"  [{badge}]  {r['country'].upper()}")
        print(f"    Known for   : {r['known_for']}")
        print(f"    Best time   : {r['best_time']}")
        print(f"    ✈ Economy flight  : ₹{r['flight']:,} / person")
        print(f"    💰 Total cost     : ₹{r['total']:,}  (₹{r['per_p']:,} / person)")
        print(f"    💵 Budget left    : ₹{r['leftover']:,}")
        print(f"    🛡 Safety         : {r['safety']}/10")
        divider()

    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more fit your budget.")

    input("\n  Press Enter to continue...")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

def run_travel_planner():
    df = load_data()

    while True:
        print_header("MAIN MENU")
        print("  [1]  Plan a trip")
        print("  [2]  Smart Recommend — find trips within your budget")
        print("  [3]  Logout")
        divider()

        choice = input("  Select option: ").strip()

        if choice == "1":
            plan_trip(df)
        elif choice == "2":
            smart_recommend(df)
        elif choice == "3":
            print("\n  Logged out. See you soon!\n")
            return
        else:
            print("  Invalid option.")
