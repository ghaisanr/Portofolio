import pandas as pd
import numpy as np
from google_play_scraper import Sort, reviews
import mysql.connector
from mysql.connector import Error

class ReviewScraper:
    def __init__(self, app_id, lang='id', country='id', sort=Sort.NEWEST, count=1000):
        self.app_id = app_id
        self.lang = lang
        self.country = country
        self.sort = sort
        self.count = count
        self.df_reviews = None

    def scrape_reviews(self):
        result, _ = reviews(
            self.app_id,
            lang=self.lang,
            country=self.country,
            sort=self.sort,
            count=self.count
        )
        # Convert results into DataFrame
        self.df_reviews = pd.DataFrame(np.array(result), columns=['review'])
        self.df_reviews = self.df_reviews.join(pd.DataFrame(self.df_reviews.pop('review').tolist()))
        print(f"Scraped {len(self.df_reviews)} reviews.")
        return self.df_reviews

class DatabaseManager:
    def __init__(self, host, database, user, password, port=3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def create_reviews_table(self):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS reviews;")
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
            cursor.close()

    def insert_reviews(self, df_reviews):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            for _, row in df_reviews.iterrows():
                cursor.execute("""
                    INSERT INTO reviews (user_name, score, content, date, version)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row['userName'], row['score'], row['content'], row['at'], row['appVersion']))
            self.connection.commit()
            print(f"{cursor.rowcount} reviews inserted.")
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed.")

# Usage example
if __name__ == "__main__":
    # Initialize and scrape reviews
    scraper = ReviewScraper(app_id="com.linkedin.android")
    df_reviews = scraper.scrape_reviews()

    # Initialize Database manager
    db_manager = DatabaseManager(
        host='localhost',
        database='reviews',
        user='root',
        password='',
        port=3306
    )
    db_manager.connect()
    db_manager.create_reviews_table()
    db_manager.insert_reviews(df_reviews)
    db_manager.close_connection()