import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="melcowe",
    port=5432
)

cur = conn.cursor()

# creating table PERSON
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS person (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender CHAR(1) NOT NULL
    );
    """
)

# inserting data into PERSON table: To avoid duplicate entries, we use `ON CONFLICT DO NOTHING`
cur.execute(
    """
    INSERT INTO person (id, name, age, gender) VALUES
    (1, 'John Doe', 30, 'M'),
    (2, 'Jane Smith', 25, 'F'),
    (3, 'Alice Johnson', 28, 'F'),
    (4, 'Bob Brown', 35, 'M')
    ON CONFLICT (id) DO NOTHING;
    """
)

# data fetching single line
cur.execute('''SELECT * FROM person WHERE name = 'John Doe';''')
print(cur.fetchone())

# data fetching multiple lines
cur.execute('''SELECT * FROM person;''')
# print(cur.fetchall()) # if you want all the data in a single line
for row in cur.fetchall(): # data in multiple lines
    print(row)

conn.commit()

cur.close()
conn.close()