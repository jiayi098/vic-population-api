from flask import Flask, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to the database
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

app = Flask(__name__)

# 1. Return welcome message
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Victoria Population API"})

# 2. Return the first 50 rows of the Victoria population table
@app.route("/population")
def get_population():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM population_VIC LIMIT 50")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

# 3. Get Melbourne City data: compare population and population density trends by SA2 name
@app.route("/population/melbourne-city")
def melbourne_city_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sa2_name, area_km2,
               y2001, y2002, y2003, y2004, y2005,
               y2006, y2007, y2008, y2009, y2010,
               y2011, y2012, y2013, y2014, y2015,
               y2016, y2017, y2018, y2019, y2020, y2021
        FROM population_VIC
        WHERE sa3_name = 'Melbourne City'
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return jsonify({"message": "No data found for Melbourne City"})

    result = []
    for row in rows:
        sa2_name = row["sa2_name"]
        area = row["area_km2"]

        # Yearly population data
        yearly_population = {year: row[f"y{year}"] for year in range(2001, 2022)}

        # Yearly population density (population / area)
        yearly_density = {}
        for year in range(2001, 2022):
            pop = row[f"y{year}"]
            yearly_density[year] = round(pop / area, 2) if area and area > 0 else None

        result.append({
            "sa2_name": sa2_name,
            "yearly_population": yearly_population,
            "yearly_density": yearly_density
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
