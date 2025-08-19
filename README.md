# 🏎 Bootcamp Rally Racing App

A simple rally racing management application built with **Snowflake**, **Python**, and **Streamlit**.  
This app allows you to manage racing teams, cars, budgets, and simulate rally races with prize distribution and entry fees.

---

## 🚀 What you can do with it

- Add new teams (with a starting budget)

- Add new cars with stats like horsepower, weight, reliability, etc.

- See all teams and their current balances

- Start a race (random track is chosen, entry fees are paid, winners get prizes)

- Budgets are updated automatically after each race

- Keep track of transactions (fees and prizes) stored in Snowflake

---

## 📂 Project Structure
app.py → the main Streamlit app

db.py → database connection + helper functions

requirements.txt → list of Python packages to install

create_tables.sql → SQL script to set up tables and sample data

.streamlit/secrets.toml → template file for Snowflake login (fill in your own credentials here)

---

## 🔧 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/VasilijsParfens/bootcamp-rally-app.git
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
