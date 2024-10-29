# Scraping a LinkedIn review in Google Play with MySQL Integration and Analyzing the Result Using Word Cloud

This project is a Python script that scrapes reviews from the Google Play Store for a specified app and stores them in a MySQL database. After the scraper, analysis will be carried out using word cloud. It utilizes the `google_play_scraper` library for scraping, `mysql-connector` for database integration, and `wordcloud` for word cloud generation.

## Features 
* Scrapes reviews from the Google Play Store for a specified app using `module`
* Stores review data in a MySQL database with columns using `module`
* Preprocessing data for word cloud generation.
* Generates a word cloud from the review data.

## Installation
web  scraping libraries: google_play_scraper
```
pip install google-play-scraper
```

mysql connector library:
```
pip install mysql-connector-python
```

word cloud library:
```
pip install wordcloud
```

## Script detail
The script is divided into the following sections:

* Import Libraries: Imports necessary libraries for scraping, data manipulation, database interaction, preprocessing data, and  word cloud generation.
* Scrape Reviews: Uses `google_play_scraper` to fetch reviews for the specified app.
* Data Transformation: Converts scraped data into a pandas DataFrame for easy manipulation.
* Database Connection: Connects to a MySQL database and creates a table named reviews if it does not exist.
* Data Insertion: Iterates over the DataFrame rows and inserts each review into the reviews table.
* preprocessing data: remove columns, case folding, tokenizing, filtering, and stemming.
* Word Cloud Generation: Uses wordcloud to generate a word cloud from the review data.

## Usage
1. Google-play-scraper
```python
from google_play_scraper import Sort, reviews

def scrape_reviews(self):
    result, _ = reviews(
            self.app_id,
            lang=self.lang,
            country=self.country,
            sort=self.sort,
            count=self.count
        )
)
```
* The country and language codes that can be included in the `lang` and `country` parameters described below depend on the [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) and [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standards, respectively. `lang` and `country` default=`id`

* `sort` for the reviews to be returned in the following order, Default=`NEWEST`

* `Count` for the number of reviews to be scraped, Default=1000.


2. MySQL Connector
Update the MySQL connection parameters in the connection object:
```python
import mysql.connector
from mysql.connector import Error

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
```


3.  Run the script
```python
if __name__ == "__main__":
    # Initialize and scrape reviews
    scraper = ReviewScraper(app_id="com.linkedin.android")
    df_reviews = scraper.scrape_reviews()

    # Initialize Database manager
    db_manager = DatabaseManager(
        host='localhost',
        database='reviews',
        user='root',
        password='Rahasia100!',
        port=3306
    )
    db_manager.connect()
    db_manager.create_reviews_table()
    db_manager.insert_reviews(df_reviews)
    db_manager.close_connection()
```
The script will scrape reviews in google play, input link to insert them into the database, and generate a word cloud. 
