# 🏎 Bootcamp Rally Racing App

A simple rally racing management application built with **Snowflake**, **Python**, and **Streamlit**.  
This app allows you to manage racing teams, cars, budgets, and simulate rally races with prize distribution and entry fees.

---

## 🚀 Features

- Manage racing teams and their budgets
- Add new teams and initialize wallets
- Add new cars with detailed performance attributes
- View current teams, cars, and balances
- Run rally race simulations:
  - Randomly selected tracks
  - Entry fee deduction
  - Randomized race results based on car stats + track difficulty
  - Automatic wallet updates (fees and prizes)
- Transaction history stored in Snowflake
- Extensible schema with clear separation of **data**, **wallet**, and **race** layers

---

## 📂 Project Structure
bootcamp-rally-app/
│── app.py # Main Streamlit app
│── db.py # Database connection + query helpers
│── requirements.txt # Python dependencies
│── .streamlit/
│ └── secrets.toml # Snowflake credentials (template provided)

---

## 🔧 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/bootcamp-rally-app.git
cd bootcamp-rally-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Snowflake credentials in .streamlit/secrets.toml (create it if needed)
A template file is included:

[snowflake]

user = "YOUR_SNOWFLAKE_USER"

password = "YOUR_SNOWFLAKE_PASSWORD"

account = "YOUR_SNOWFLAKE_ACCOUNT"

warehouse = "YOUR_SNOWFLAKE_WAREHOUSE"

database = "BOOTCAMP_RALLY"

### 4. Run the Streamlit app

```bash
streamlit run app.py
```
schema = "PUBLIC"

