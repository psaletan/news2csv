#!/usr/bin/env python3
"""news2csv.py
Download recent articles list from my newspapers
"""

# Python libraries
import os
import csv
import datetime
import time
import re
from operator import itemgetter
from urllib.parse import urlparse

# Third party libraries
import newspaper

# Project custom libraries
import news2csv_config as config

class ArticleRecord(object):
    """Single news article"""

    def __init__(self, article, site, history):
        self.article = article
        self.site = site
        self.domain = urlparse(self.article.url).netloc
        self.is_eligible = self.domain in self.site.domains
        self.is_new = self.article.url not in history.urls
        self.url_has_params = True if self.article.url.find('.html?') > -1 else False
        self.got_download = False

    def get_download(self):
        """Download and parse a single article"""
        # Download only articles that match the main news domains and haven't been downloaded before.
        # If URL has GET parameters at the end, we won't download it
        if (self.is_eligible) and (self.is_new) and (not self.url_has_params):
            print('\n' + self.article.url)
            self.article.download()
            # Wait for download to finish.  See: https://github.com/codelucas/newspaper/issues/357
            seconds = 0
            while self.article.download_state == 0:
                time.sleep(1)
                seconds += 1
                if seconds >= config.DOWNLOAD_WAIT_LIMIT:
                    self.got_download = False
                    break
        self.got_download = (self.article.download_state != 0)
        return self.got_download

    def prepare(self):
        """Prepare article as dictionary of fields; parse and compute fields."""
        try:
            self.article.parse()
            self.rec = {}
            self.rec['run_time'] = config.RUN_TIME
            self.rec['domain'] = self.domain
            # Parse the URL to determine the article's section (e.g. news, opinion, ...).
            # Different sites have different regex patterns.
            self.rec['section'] = re.sub(self.site.left_cut_regex, '', re.sub(self.site.right_cut_regex, '', self.article.url))
            # We create an empty Flag field, for end user to mark/prioritize which articles to read.
            self.rec['flag'] = ''
            self.rec['authors'] = ', '.join(self.article.authors)
            self.rec['title'] = self.article.title
            self.rec['url'] = self.article.url
            # Delete any time string from end of the publish date.  It's usually 00:00:00.
            if self.article.publish_date is not None:
                self.rec['publish_date'] = self.article.publish_date.strftime('%Y-%m-%d')
            else:
                self.rec['publish_date'] = ''
            self.rec['meta_description'] = self.article.meta_description
            # Natural language processing
            self.article.nlp()
            # TODO: Include article summary? Will need to strip/replace newlines.
            #self.rec['summary'] = article.summary
            self.rec['keywords'] = ', '.join(self.article.keywords)
            success = True
        except:
            success = False
        return success

    def write_rec(self, file_name=config.OUTPUT_FILE):
        """Write single downloaded article record to CSV file."""
        print(self.rec)
        write_mode = 'a' if os.path.exists(file_name) else 'w'
        with open(file_name, write_mode) as csvfile:
            fieldnames = ['run_time', 'domain', 'publish_date', 'section',
                'flag', 'title', 'authors',
                'url', 'meta_description', 'keywords']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='',
                extrasaction="ignore")
            if write_mode == 'w':
                writer.writeheader()
            writer.writerow(self.rec)
        return

class NewsSite(object):
    """News site object.  Stores lists of past, current articles."""

    def __init__(self, src):
        self.url = src['url']
        self.domains = src['domains']
        self.left_cut_regex =src['left_cut_regex']
        self.right_cut_regex =src['right_cut_regex']
        self.paper = newspaper.build(self.url, language=config.LANGUAGE, memoize_articles=config.MEMOIZE_ARTICLES)

class ArticleHistory(object):
    """Past history: record of what has been downloaded."""

    def __init__(self, history_file=config.OUTPUT_FILE):
        self.history_file = history_file
        self.urls = self.get_previously_downloaded_articles()

    def get_previously_downloaded_articles(self):
        """Get list of previously downloaded articles -- identify uniquely by URL."""
        urls = []
        if not os.path.exists(self.history_file):
            return urls
        with open(self.history_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames
            for row in reader:
                url = row['url']
                urls.append(url)
            return urls

def main():
    """Main program loop."""

    history = ArticleHistory(config.OUTPUT_FILE)

    for src in config.NEWS_SOURCES:
        site = NewsSite(src)
        print('\n' + site.url, site.paper.size())
        total_count = 0
        success_count = 0
        for article in site.paper.articles:
            r = ArticleRecord(article, site, history)
            if r.get_download():
                if r.prepare():
                    r.write_rec()
                    success_count += 1
            total_count += 1
            if total_count >= config.ARTICLE_LIMIT:
                break

if __name__ == "__main__":
    main()
