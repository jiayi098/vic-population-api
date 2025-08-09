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
    return jsonify({"message": "Welcome to the Melbourne City Population API"})

# 2. Return the rows of the melbourne city
@app.route("/melbourne-city")
def melbourne_city():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM population_VIC
        WHERE sa3_name = 'Melbourne City'
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

# 3. Get subregions of melbourne city
@app.route("/melbourne-city/subregions")
def melbourne_city_subregions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT sa2_name
        FROM population_VIC
        WHERE sa3_name = 'Melbourne City'
    """)
    rows = [row["sa2_name"] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(rows)

# 4. Get population trends for subregions
@app.route("/melbourne-city/population-trends")
def melbourne_city_population_trends():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sa2_name, y2001, y2002, y2003, y2004, y2005,
               y2006, y2007, y2008, y2009, y2010,
               y2011, y2012, y2013, y2014, y2015,
               y2016, y2017, y2018, y2019, y2020, y2021
        FROM population_VIC
        WHERE sa3_name = 'Melbourne City'
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for row in rows:
        yearly_pop = {year: row[f"y{year}"] for year in range(2001, 2022)}
        result.append({
            "sa2_name": row["sa2_name"],
            "yearly_population": yearly_pop
        })

    return jsonify(result)

# 5. Get population density trends for subregions
@app.route("/melbourne-city/density-trends")
def melbourne_city_density_trends():
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

    result = []
    for row in rows:
        densities = {year: round(row[f"y{year}"] / row["area_km2"], 2)
                     if row["area_km2"] else None
                     for year in range(2001, 2022)}
        result.append({
            "sa2_name": row["sa2_name"],
            "yearly_density": densities
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
