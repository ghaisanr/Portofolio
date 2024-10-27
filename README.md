# Scraping linkedin review in google play with MySQL Integration and Analyze The Result using Word Cloud

This project is a Python script that scrapes reviews from the Google Play Store for a specified app and stores them in a MySQL database. After the scraper, analysis will be carried out using word cloud. It utilizes the `google_play_scraper` library for scraping, `mysql-connector` for database integration, and `wordcloud` for word cloud generation.

## Features 
* Scrapes reviews from the Google Play Store for a specified app.
* Stores review data in a MySQL database with columns.
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
1. Google-play-screper
```python
from google_play_scraper import Sort, reviews

result, continuation_token = reviews(
    "com.linkedin.android",
    lang="id",
    country="id",
    sort=Sort.NEWEST,
    count=1000
)
```
* The country and language codes that can be included in the `lang` and `country` parameters described below depend on the [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) and [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standards, respectively.

* sort for  the reviews to be returned in the following order: `NEWEST`

* Count for  the number of reviews to be scraped.


2. MySQL Connector
Update the MySQL connection parameters in the connection object:
```python
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host='localhost',
    database='review',
    user='root',
    password='your_password',
    port=3306
)
```


3.  Run the script
```bash
python script.py
```
The script will scrape reviews, insert them into the database, and generate a word cloud. 
