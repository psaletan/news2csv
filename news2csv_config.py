"""news2csv_config.py
News sources and settings for use with newspaper3k library.
"""

import os
import datetime

LANGUAGE = 'en'

# List URL's of online news source sites
NEWS_SOURCES = [

    { 'url': 'https://nytimes.com', 'domains': ['www.nytimes.com'],
        'left_cut_regex': r'/.*', 'right_cut_regex': r'.*nytimes.com/\d\d\d\d/\d\d/\d\d/' },

    { 'url': 'https://www.washingtonpost.com', 'domains': ['www.washingtonpost.com'],
        'left_cut_regex': r'/.*', 'right_cut_regex': r'.*washingtonpost.com/' },

]

# Include only these domains within the sites
#INCLUDE_DOMAINS = [
#    'www.washingtonpost.com',
#    'www.nytimes.com',
#]

# Set to zero for unrestricted numbers of days, articles
RECENT_DAYS = 0
ARTICLE_LIMIT = 0
MEMOIZE_ARTICLES = False
DOWNLOAD_WAIT_LIMIT = 30

# Where to download files
OUTPUT_DIR = "/home/paul/Downloads"
CSV_OUTPUTFILE = "news.csv"

# Calculated config variables based on the above constants
RUN_TIME = datetime.date.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, CSV_OUTPUTFILE)
ARTICLE_LIMIT = ARTICLE_LIMIT if ARTICLE_LIMIT > 0 else 9999
