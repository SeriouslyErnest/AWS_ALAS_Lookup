
## run: pip install feedparser, bs4, pytz, time
#other dependencies: sqlite3, re
#for demo, clear last_run.json
#for production, change init_url and update_url
#remember to remove the #debug updated_ids after demo
#when new system: ensure config.json path in smtp is correct

import tkinter as tk
from init_parse import initial_setup
from main_parse import update_parser
from gui_id_search import id_search_ui
from gui_libsearch import lib_search_ui
from gui_stats import lib_stats
from gui_rsstools import rss_tools
import json


status_messages = {
    "Search by ID": "ID search completed.",
    "Search by Library": "Library search completed.",
    "Component Stats": "Component stats completed.",
    "First time setup": "First time setup completed.",
    "Check for Updates (update last_run for demo)": "Check for Updates completed."
}

def update_status_message(message):
    status_label.config(text=message)

def run_id_search():
    id_search_ui()  # Run ID search function
    update_status_message(status_messages["Search by ID"])

def run_lib_search():
    lib_search_ui()  # Run Library search function
    update_status_message(status_messages["Search by Library"])

def run_lib_stats():
    lib_stats()  # Run Component stats function
    update_status_message(status_messages["Component Stats"])

def run_first_time_setup(url):
    initial_setup(url)  # Call the initial setup function from init_parse module
    update_status_message(status_messages["First time setup"])

def run_check_for_updates(url):
    update_parser(url)
    update_status_message(status_messages["Check for Updates (update last_run for demo)"])

def rss_utils():
    rss_tools()  # Run ID search function
    update_status_message(status_messages["RSS Tools"])

def main():
    global root
    root = tk.Tk()
    root.title("ALAS Database Tool")  # Set the title for the main interface
    
    # Calculate the width of the title to set the minimum size
    title_width = len("ALAS Database Tool") * 10  # Adjust the multiplier according to the font size
    
    # Set minimum size for the interface
    root.minsize(title_width, 200)  # Set a minimum width and height for the interface
    
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        rss_url = config_data.get('rss_url', 'No URL found')


    #for production, both init and update URLs to be the same main URL
    # init_url = 'alas_test.rss'
    init_url = rss_url
    #init_url = 'https://alas.aws.amazon.com/AL2/alas.rss'
    update_url = init_url
    # print("update url", update_url)
    # update_url = 'alas_test_updated.rss'
    #note that depending on AL1 or AL2, choose the correct RSS. AL2 uses https://alas.aws.amazon.com/AL2/alas.rss
    # as of Apr 2024 update, this is controlled in config.json and in button 6 "rss_utils"
    print("rss", rss_url)
    print("init", init_url)
    print("update", update_url)
    # Buttons for each function
    button1 = tk.Button(root, text="Search by ID", command=run_id_search)
    button1.pack()

    button2 = tk.Button(root, text="Search by Library", command=run_lib_search)
    button2.pack()

    button3 = tk.Button(root, text="Component Stats", command=run_lib_stats)
    button3.pack()

    button4 = tk.Button(root, text="First time setup", command=lambda: run_first_time_setup(init_url))
    #note: drops existing databases to run. 
    button4.pack()

    button5 = tk.Button(root, text="Check for Updates (update last_run for demo)", command=lambda: run_check_for_updates(update_url))
    #note: uses last_run.json to check time of last run and process only updated libs. Backdate to 1999 for demo
    button5.pack()

    button6 = tk.Button(root, text="Check or Edit RSS source URL", command=rss_utils)
    button6.pack()

    global status_label
    status_label = tk.Label(root, text="")
    status_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
