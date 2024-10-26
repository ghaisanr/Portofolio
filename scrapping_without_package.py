from google_play_scraper import Sort, reviews
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error

# Scraping the reviews
result, continuation_token = reviews(
    "com.linkedin.android",
    lang="id",
    country="id",
    sort=Sort.NEWEST,
    count=100
)

# Convert the result into a DataFrame
df_busu = pd.DataFrame(np.array(result), columns=['review'])
df_busu = df_busu.join(pd.DataFrame(df_busu.pop('review').tolist()))

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='review',
        user='root',
        password='emma123',
        port=3306
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Drop the existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS reviews;")

        # Create a new table with the version column
        cursor.execute("""
            CREATE TABLE reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(255),
                score INT,
                content TEXT,
                date DATETIME,
                version TEXT
            )
        """)
        print("Table 'reviews' created successfully.")

          # Insert the reviews into the database
        for index, row in df_busu.iterrows():
            cursor.execute("""
                INSERT INTO reviews (user_name, score, content, date, version)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['userName'], row['score'], row['content'], row['at'], row['appVersion']))  # Ensure 'appVersion' exists

        # Commit the transaction
        connection.commit()
        print(f"{cursor.rowcount} reviews inserted.")

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")