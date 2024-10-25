from sqlalchemy import create_engine

# Create a SQLAlchemy engine
engine = create_engine("mysql+mysqlconnector://root:emma123@localhost:3306/linkedin_review")

from google_play_scraper import Sort, reviews
import pandas as pd
import numpy as np

# Scraping the reviews
result, continuation_token = reviews(
    "com.linkedin.android",
    lang="id",
    country="id",
    sort=Sort.NEWEST,
    count=1000
)

# Convert the result into a DataFrame
df = pd.DataFrame(np.array(result), columns=['review'])
df = df.join(pd.DataFrame(df.pop('review').tolist()))

# Saving the DataFrame to SQL
try:
    df.to_sql('linkedin_review', con=engine, if_exists='replace', index=False)
    print("Data has been saved to the database successfully.")
except Exception as e:
    print("An error occurred:", e)

    # Querying data to confirm
query_result = pd.read_sql("SELECT * FROM linkedin_review LIMIT 5", con=engine)
print(query_result)

#saving the Dataframe to  csv file
df.to_csv('data scraping linkedin.csv', index=False)

