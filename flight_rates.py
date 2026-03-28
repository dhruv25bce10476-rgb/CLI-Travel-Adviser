# flight_rates.py
import datetime

# Base flight prices (INR) from India — separated from CSV
BASE_RATES = {
    "Japan":        35000,
    "France":       30000,
    "USA":          45000,
    "UAE":          12000,
    "Thailand":     10000,
    "Australia":    55000,
    "Germany":      32000,
    "Singapore":    16000,
    "Canada":       50000,
    "Italy":        31000,
    "Spain":        30000,
    "Netherlands":  33000,
    "South Korea":  28000,
    "Turkey":       22000,
    "Malaysia":     14000,
    "Indonesia":    18000,
    "UK":           38000,
    "Switzerland":  40000,
    "New Zealand":  58000,
    "Vietnam":      13000,
}

# Price tiers with suggested options
PRICE_TIERS = {
    "Economy":   0.88,   # ~12% cheaper (advance booking / budget airline)
    "Standard":  1.00,
    "Flexible":  1.15,   # changeable tickets
    "Business":  2.80,
}

def get_flight_options(country: str) -> dict:
    """
    Returns simulated flight price options for a country.
    Adds hourly fluctuation to simulate live rates.
    """
    base = BASE_RATES.get(country, 30000)

    # Simulate ±8% market fluctuation based on hour of day
    hour = datetime.datetime.now().hour
    seed = (ord(country[0]) + hour * 7) % 17  # 0–16
    jitter = (seed - 8) / 100                 # -0.08 to +0.08
    live_base = round(base * (1 + jitter) / 500) * 500  # round to nearest 500

    options = {}
    for tier, multiplier in PRICE_TIERS.items():
        options[tier] = round(live_base * multiplier / 500) * 500

    return options

def display_flight_options(country: str) -> int:
    """
    Displays flight price tiers and returns the chosen price per person.
    """
    options = get_flight_options(country)

    print(f"\n  ✈  Live Flight Rates to {country} (from India)")
    print("  " + "─" * 41)
    for i, (tier, price) in enumerate(options.items(), 1):
        tag = ""
        if tier == "Economy":
            tag = "  ← best deal"
        elif tier == "Standard":
            tag = "  ← most popular"
        print(f"  [{i}] {tier:<12}  ₹{price:>8,}{tag}")
    print("  " + "─" * 41)

    while True:
        try:
            choice = int(input("  Select fare class (1-4): "))
            if 1 <= choice <= 4:
                tier = list(options.keys())[choice - 1]
                price = options[tier]
                print(f"\n  ✓ Selected: {tier} class — ₹{price:,} per person")
                return price
            else:
                print("  Enter a number between 1 and 4.")
        except ValueError:
            print("  Please enter a valid number.")
