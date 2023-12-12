# old repo: aws_alas
Something to collect ALAS alerts and check if your vulnerabilities are listed in it. 
Instructions: unzip in local folder, run pip install for dependencies, and python main.py to launch menu.
Run first time setup in menu, and you can then search package -> ALAS, CVE, ALAS date updated, or ALAS -> package, CVE, ALAS date updated.
## run: pip install feedparser, bs4, pytz
#other dependencies: sqlite3, re
#for demo, clear last_run.json
#when new system: ensure config.json path in smtp is correct

## if you want email functionalities, open config.json and add in your email address/ password there. 


This is a simple personal project to make my life easier because I need to search for ALAS <-> package manually one by one. Hope it helps someone else out there. 