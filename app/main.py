import streamlit as st
import pandas as pd
import random
from db import run_query, run_command

st.set_page_config(page_title="Bootcamp Rally Racing", page_icon="🏁", layout="centered")
st.title("🏎️ Bootcamp Rally Racing App")


# SHOW TEAMS + BALANCES

st.header("Teams and Wallets 💰")

teams = run_query("""
    SELECT t.id, t.team_name, t.country, w.balance 
    FROM data.team t 
    JOIN wallet.team_balance w ON t.id = w.team_id
""")
teams.columns = teams.columns.str.lower()
st.dataframe(teams)


# ADD NEW TEAM (Bonus)

st.header("Add New Team 🏆")

with st.form("add_team_form"):
    team_name = st.text_input("Team Name")
    country = st.text_input("Country")
    start_balance = st.number_input("Starting Balance", min_value=0, value=5000)
    submit_team = st.form_submit_button("Add Team")

    if submit_team:
        # insert team
        run_command("""
            INSERT INTO data.team (team_name, country)
            VALUES (%(team_name)s, %(country)s)
        """, {"team_name": team_name, "country": country})

        # fetch the new team_id
        new_team_id = run_query("SELECT MAX(id) AS team_id FROM data.team").iloc[0, 0]

        # initialize wallet
        run_command("""
            INSERT INTO wallet.team_balance (team_id, balance)
            VALUES (%(team_id)s, %(balance)s)
        """, {"team_id": int(new_team_id), "balance": float(start_balance)})

        st.success(f"Team '{team_name}' added with balance {start_balance} 💰")

# ADD NEW CAR

st.header("Add New Car 🚗")

with st.form("add_car_form"):
    team_id = st.number_input("Team ID", min_value=1)
    manufacturer_id = st.number_input("Manufacturer ID", min_value=1)
    model = st.text_input("Model")
    year = st.number_input("Year", min_value=1990, max_value=2030, value=2020)
    hp = st.number_input("Horsepower", min_value=50, max_value=1000, value=300)
    weight = st.number_input("Weight (kg)", min_value=500, max_value=2000, value=1400)
    accel = st.number_input("0-100 Accel (sec)", min_value=1.0, max_value=10.0, value=5.0)
    top_speed = st.number_input("Top Speed (kmh)", min_value=100, max_value=400, value=250)
    reliability = st.slider("Reliability", 0.0, 1.0, 0.8)
    aero = st.slider("Aero", 0.0, 1.0, 0.7)
    drivetrain = st.selectbox("Drivetrain", ["AWD", "RWD", "FWD"])
    tire = st.text_input("Tire type", "Tarmac")
    submit_car = st.form_submit_button("Add Car")

    if submit_car:
        run_command("""
            INSERT INTO data.car (team_id, manufacturer_id, model, year, hp, weight, accel, top_speed, reliability, aero, drivetrain, tire)
            VALUES (%(team_id)s, %(manufacturer_id)s, %(model)s, %(year)s, %(hp)s, %(weight)s, %(accel)s, %(top_speed)s, %(reliability)s, %(aero)s, %(drivetrain)s, %(tire)s)
        """, {
            "team_id": team_id,
            "manufacturer_id": manufacturer_id,
            "model": model,
            "year": year,
            "hp": hp,
            "weight": weight,
            "accel": accel,
            "top_speed": top_speed,
            "reliability": reliability,
            "aero": aero,
            "drivetrain": drivetrain,
            "tire": tire
        })
        st.success(f"Car {model} added to Team {team_id}!")


# START RACE (SAVE RESULTS)

st.header("Start Race 🏁")

if st.button("Go!"):
    # pick random track
    track = run_query("SELECT id, name, difficulty FROM data.track ORDER BY RANDOM() LIMIT 1").iloc[0]
    track_id = track["ID"]
    track_name = track["NAME"]
    track_difficulty = track["DIFFICULTY"]

    # create race event
    entry_fee = 1000
    prize_pool = 3000
    # insert race event
    run_command("""
        INSERT INTO races.race (track_id, entry_fee, prize_pool) 
        VALUES (%(track_id)s, %(entry_fee)s, %(prize_pool)s)
    """, {"track_id": track_id, "entry_fee": entry_fee, "prize_pool": prize_pool})

    # fetch last race_id
    race_id = run_query("SELECT MAX(id) AS race_id FROM races.race").iloc[0, 0]

    cars = run_query("""
        SELECT c.id, c.team_id, c.model, c.hp, c.weight, c.accel, c.reliability, c.aero
        FROM data.car c
    """)
    cars.columns = cars.columns.str.lower()

    results = []
    for _, car in cars.iterrows():
        base_time = 100 / (car["hp"] / car["weight"]) * 10
        randomness = random.uniform(0.9, 1.1)
        difficulty_penalty = 1 + track_difficulty * random.uniform(0.1, 0.3)
        time = base_time * randomness * difficulty_penalty
        results.append((car["id"], car["team_id"], car["model"], time))

    # rank by time
    results.sort(key=lambda x: x[3])
    rewards = [prize_pool * 0.5, prize_pool * 0.3, prize_pool * 0.2]

    output = []
    for pos, (car_id, team_id, model, time) in enumerate(results, start=1):
        reward = rewards[pos-1] if pos <= 3 else 0
        fee = entry_fee

        # save result
        run_command("""
            INSERT INTO races.result (race_id, car_id, team_id, position, time_minutes, reward, penalty)
            VALUES (%(race_id)s, %(car_id)s, %(team_id)s, %(pos)s, %(time)s, %(reward)s, %(penalty)s)
        """, {
            "race_id": race_id,
            "car_id": car_id,
            "team_id": team_id,
            "pos": pos,
            "time": time,
            "reward": reward,
            "penalty": fee
        })

        # update wallet balance
        run_command("""
            UPDATE wallet.team_balance
            SET balance = balance + %(reward)s - %(fee)s
            WHERE team_id = %(team_id)s
        """, {"reward": reward, "fee": fee, "team_id": team_id})

        # record fee txn
        run_command("""
            INSERT INTO wallet.transaction (team_id, txn_type, amount, balance_after)
            SELECT %(team_id)s, 'fee', -%(fee)s, balance
            FROM wallet.team_balance WHERE team_id = %(team_id)s
        """, {"team_id": team_id, "fee": fee})

        # record prize txn (if any)
        if reward > 0:
            run_command("""
                INSERT INTO wallet.transaction (team_id, txn_type, amount, balance_after)
                SELECT %(team_id)s, 'prize', %(reward)s, balance
                FROM wallet.team_balance WHERE team_id = %(team_id)s
            """, {"team_id": team_id, "reward": reward})

        output.append([pos, model, round(time, 2), reward])

    # show results
    df = pd.DataFrame(output, columns=["Position", "Car", "Time", "Reward"])
    st.subheader(f"Track: {track_name}")
    st.dataframe(df)
    st.success(f"Race finished and saved! (Race ID: {race_id}) ✅")
