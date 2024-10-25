from google_play_scraper import app

import pandas as pd
import numpy as np

# Scrape desired number of reviews
from google_play_scraper import Sort, reviews

result, continuation_token = reviews(
    "com.linkedin.android",

    lang="id",  # defaults to 'en'
    country="id",  # defaults to 'us'

    sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
    count=100,  # defaults to 100

    filter_score_with=None  # defaults to None (means all score) Use 1 or 2 or 3 or 4 or 5 to select certain score
)

df_busu = pd.DataFrame(np.array(result), columns=['review'])

df_busu = df_busu.join(pd.DataFrame(df_busu.pop('review').tolist()))

print(df_busu.tail())