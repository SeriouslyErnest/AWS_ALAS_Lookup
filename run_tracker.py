#this module is for tracking when the last update was carried out
from datetime import datetime
import json
import feedparser


# Function to load the last run date from a JSON file
def load_last_run_date():
    print("load last run")
    try:
        with open('last_run.json', 'r') as file:
            data = json.load(file)
            raw_last_run = data.get('last_run_date')
            last_run_date = datetime.strptime(raw_last_run,'%Y-%m-%d %H:%M:%S')
            return last_run_date
    except FileNotFoundError:
        # Return a default date if the file doesn't exist
        print("Note: no existing run found.")
        return None

# Function to save the last run date to a JSON file
def save_last_run_date():
    #updated to use .utcnow() rather than now()
    data = {'last_run_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
    with open('last_run.json', 'w') as file:
        json.dump(data, file)


def testrun():
    # Retrieve the last run date from the JSON file
    last_run_date = load_last_run_date()

    # URL of the RSS feed
    rss_url = 'https://alas.aws.amazon.com/AL2/alas.rss'
    feed = feedparser.parse(rss_url)

    # Compare publication dates with the last run date
    for entry in feed.entries:
        entry_date = datetime(*entry.published_parsed[:6])
        if last_run_date is None or entry_date > last_run_date:
            # There is a new update, do something
            print(f"New update found: {entry_date}")

    save_last_run_date()



def main():
    testrun()



if __name__ == '__main__':
    main()




