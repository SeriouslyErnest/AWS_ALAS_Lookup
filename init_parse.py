import feedparser
# import sqlite3
# import re
# import libs
from bs4_scrape import scrapedate, scrapelibs
from main_parse import title_details
from db_tools import write_to_alas_db, write_to_lib_db, drop_db, create_alas_db, create_lib_db
from run_tracker import save_last_run_date, load_last_run_date
from datetime import datetime
from main_parse import parser
import time 
import concurrent.futures


#note: db name is rss.db
#for reference on structure: 
# title link description pubDate

#moved to consolidate under main_parse
# def title_details(title):
#     #suggested pattern to split: <title>ALAS-2023-2285 (important): python-reportlab</title>
#     pattern = r'ALAS-(\d+-\d+) \((\w+)\): (.+)'
#     match = re.match(pattern, title)
#     if match:
#         #testing
#         print(f'ALAS-{match.group(1)}')
#         print(match.group(2))
#         print(match.group(3))
#         #regex to only identify ALAS-type alerts. Returned statement for ID to follow full ALAS notation. 
#         return f'ALAS-{match.group(1)}', match.group(2), match.group(3)
#     else:
#         #testing
#         print("no match")
#         return None, None, None
    

# def initparse(url):
#     #counter for number of entries
#     start = time.time()
#     count = 0
#     print("initparse testing",url)

#     # patch = 0
#     #parse RSS feed
#     feed = feedparser.parse(url)
#     for entry in feed.entries:
#         count += 1
#         print("initparse count", count)
#         # print("initparse entry debug", entry)
#         parser(entry)

#     save_last_run_date()
#     print("Initialization parse complete.")
#     print("Total number of ALAS entriesadded:", count)
#     end = time.time()
#     print("Time taken:", end - start)

def initparse(url):
    start = time.time()
    count = 0
    print("initparse testing", url)

    feed = feedparser.parse(url)

    # Define a function to process an entry using parser()
    def process_entry(entry):
        nonlocal count
        count += 1
        print("initparse count", count)
        parser(entry)

    # Use ThreadPoolExecutor to run parser() for each entry in parallel
    # note: use max_workers if you need to throttle number of threads. 
    # note: main resource is usually your disk write speed. 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_entry, feed.entries)

    save_last_run_date()
    print("Initialization parse complete.")
    print("Total number of ALAS entries added:", count)
    end = time.time()
    print("Time taken:", end - start)


def initial_setup(url):
    print("First time setup starting")
    drop_db('alas.db')
    drop_db('alas_lib.db')
    print("Existing DB dropped")
    create_alas_db()
    create_lib_db()
    print("DB creation completed. Proceeding to process URL: ", url)
    #demo URL
    # url = 'alas_test.rss'
    #url = 'https://alas.aws.amazon.com/AL2/alas.rss'
    # url= 'alas.aws.amazon.com_alas_20231014.rss'
    initparse(url)

def main():
    print("testing")
    #these drop the existing DB when testing
    drop_db('alas.db')
    drop_db('alas_lib.db')
    create_alas_db()
    create_lib_db()
    #url = 'https://alas.aws.amazon.com/AL2/alas.rss'
    #local path for testing
    # url= 'alas.aws.amazon.com_alas_20231014.rss'



    #short RSS for dev
    url = 'alas_test.rss'

    initparse(url)



if __name__ == '__main__':
    main()
