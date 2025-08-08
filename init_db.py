import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

print(" Connecting to the database...")
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print(" Successfully connected to the database.")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS population_VIC")

cursor.execute("""
CREATE TABLE IF NOT EXISTS population_VIC (
    st_code VARCHAR(10),
    st_name VARCHAR(100),
    gccsa_code VARCHAR(10),
    gccsa_name VARCHAR(100),
    sa4_code VARCHAR(10),
    sa4_name VARCHAR(100),
    sa3_code VARCHAR(10),
    sa3_name VARCHAR(100),
    sa2_code VARCHAR(20),
    sa2_name VARCHAR(100),
    y2001 INT, y2002 INT, y2003 INT, y2004 INT, y2005 INT,
    y2006 INT, y2007 INT, y2008 INT, y2009 INT, y2010 INT,
    y2011 INT, y2012 INT, y2013 INT, y2014 INT, y2015 INT,
    y2016 INT, y2017 INT, y2018 INT, y2019 INT, y2020 INT,
    y2021 INT,
    area_km2 FLOAT
);
""")
conn.commit()

print(" Reading the CSV file...")
import csv

# import csv file
with open("Estimated_resident_population_in_VIC.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  
    for row in reader:
        cursor.execute("""
            INSERT INTO population_VIC (
                st_code, st_name, gccsa_code, gccsa_name, sa4_code, sa4_name,
                sa3_code, sa3_name, sa2_code, sa2_name,
                y2001, y2002, y2003, y2004, y2005,
                y2006, y2007, y2008, y2009, y2010,
                y2011, y2012, y2013, y2014, y2015,
                y2016, y2017, y2018, y2019, y2020,
                y2021, area_km2
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s)
        """, row)

conn.commit()




cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
print("The datatable is:", tables)

cursor.execute("SELECT COUNT(*) FROM population_VIC")
print("Total rows inserted:", cursor.fetchone()[0])


cursor.close()
conn.close()
