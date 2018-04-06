"""news2csv_config.py
News sources and settings for use with newspaper3k library.
"""

import os
import datetime

LANGUAGE = 'en'

# URL's of online news source sites:
#   url: The main URL for the site, expected by the Newspaper3k library when building a list of articles.
#   domains: The (sub)domains to include from the main URL.  You may want to exclude foreign/lcoal stories.
#   left_cut_regex: regular expression.  Matching text will be cut from the left side of the URL
#     to expose the section name.
#   right_cut_regex: regular expression.  Matching text will be cut from the right side of the URL
#     to expose the section name.
NEWS_SOURCES = [

    { 'url': 'https://nytimes.com', 'domains': ['www.nytimes.com'],
        'left_cut_regex': r'/.*', 'right_cut_regex': r'.*nytimes.com/\d\d\d\d/\d\d/\d\d/' },

    { 'url': 'https://www.washingtonpost.com', 'domains': ['www.washingtonpost.com'],
        'left_cut_regex': r'/.*', 'right_cut_regex': r'.*washingtonpost.com/' },

]

# Set to zero for unrestricted numbers of days, articles
# TO DO: search only recent days when building the list of previously downloaded articles
#RECENT_DAYS = 0
ARTICLE_LIMIT = 0
# See Newspaper3k documentation.  MEMOIZE_ARTICLES = False means ignore its cache
MEMOIZE_ARTICLES = False
# How many seconds to wait before giving up on downloading each article
DOWNLOAD_WAIT_LIMIT = 30

# Where to download files
OUTPUT_DIR = "/home/paul/Downloads"
CSV_OUTPUTFILE = "news.csv"

# Calculated config variables based on the above constants
RUN_TIME = datetime.date.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, CSV_OUTPUTFILE)
ARTICLE_LIMIT = ARTICLE_LIMIT if ARTICLE_LIMIT > 0 else 9999
