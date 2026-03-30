#  DW Travel Adviser — CLI 

This is a Python terminal app that helps to plan international trips from India. Compare destinations, get live-simulated flight prices across fare classes, and find trips within your budget.

---

## Project Structure

```
DW Travel Adviser — CLI/
│
├── Project_Report.pdf # Project Report
├── main.py            # Entry point — run this
├── auth.py            # Login & signup system
├── traveladviser.py   # Trip planner & smart recommender
├── flight_rates.py    # Flight price engine (separated from CSV)
├── Travel_list.csv    # Destination data (hotels, visa, safety, etc.)
└── users.json         # Auto-created when first user signs up
```

---

## Requirements

- Python 3.7+
- pandas

Install dependency:
```bash
pip install pandas
```

---

## How to Run

1. Place all files in the same folder
2. Open terminal in that folder
3. Run:

```bash
python main.py
```

---

## Auth System

- **Sign Up** — create an account with email, name, username & password
- **Login** — passwords are SHA-256 hashed, 3 attempts allowed
- User data is saved in `users.json` (auto-created on first signup)

---

## Features

### 1. Plan a Trip
- Browse 20 international destinations with safety ratings
- Choose a **fare class** for your flight:

  | Fare Class | Description         |
  |------------|---------------------|
  | Economy    | Best deal           |
  | Standard   | Most popular        |
  | Flexible   | Changeable ticket   |
  | Business   | Premium comfort     |

- Enter number of rooms & nights
- Get a full cost breakdown:
  - Flight total
  - Hotel total
  - Miscellaneous expenses
  - Visa cost
  - Grand total + per person cost
  - Budget tier (Budget / Mid-Range / Premium)
  - Safety advisory

### 2. Smart Recommender
- Enter your **total budget**, number of **persons**, and **nights**
- App filters all destinations that fit your budget
- Results ranked by **safety first, then cost**
- Shows top 5 picks with leftover budget

---

## Destinations Available

Japan, France, USA, UAE, Thailand, Australia, Germany, Singapore, Canada, Italy, Spain, Netherlands, South Korea, Turkey, Malaysia, Indonesia, UK, Switzerland, New Zealand, Vietnam

---

## Notes

- Flight prices simulate hourly market fluctuation (±8%) — refresh each session for updated rates
- Flight data is **not** stored in the CSV; it lives in `flight_rates.py` for easy updates
- To add a new destination: add a row to `Travel_list.csv` and a base flight price in `flight_rates.py`

---

## Author

Made by **Dhruv Prasad Warrier**  
DW Travel Adviser
