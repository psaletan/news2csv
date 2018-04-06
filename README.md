# News2Csv: Download online news articles to a CSV file

This repository contains a python3 command-line application that downloads
a list of current articles, using the
[Newspaper3k](https://github.com/codelucas/newspaper) library for scraping
news sites.

The articles are appended to a CSV file for ease in importing them to a
spreadsheet or database.  Each row contains fields like the title, URL,
author and meta description.  It doesn't include the full text of the
article.  The CSV file is also used to determine which articles have
previously been downloaded and skip them.

## Installation

Install the Newspaper3k for Python and its dependencies:

    $ pip3 install -r requirements.txt

## Configuration

Edit `news2csv_config.py`.  Change the values for `OUTPUT_DIR` and
`CSV_OUTPUTFILE`  to set the respective path and filename of your CSV
file.  If the file doesn't exist, it will be created at run-time.

The config file has settings for the New York Times and Washington Post.
Add to this list or delete as you like.  The `left_cut_regex` and
`right_cut_regex` keys expect regular expression values, used to parse
the section name (e.g. news, opinion, sports) from the URL.  You can
set them to empty ('') if you don't care about this field.

## Execution

    $ cd <DIRECTORY_WHERE_YOU_CLONED_THIS_REPO>
    $ ./news2csv.py

The article URL's and their data will be printed to the console as each is
downloaded.

## Viewing

The generated CSV file has these fields, most of them copied from the
Articles objects populated by the Newspaper3k library.  If the field
isn't explained below, see the
[newspaper documentation](http://newspaper.readthedocs.io/en/latest/)
for the definition.

* `run_time`: The time that the application started.  The same timestamp
is applied
to all articles downloaded during this run.
* `domain`: The domain name, parsed from the URL.
* `publish_date`: Date of publication, with the time omitted.
* `section`: Section name, parsed from the URL (see regex notes above).
* `flag`: An empty field for the end user to mark/prioritize/etc which
articles to read.
* `title`
* `authors`
* `url`
* `meta_description`
* `keywords`
