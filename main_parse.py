#remember to remove the #debug updated_ids
import feedparser
import re
from run_tracker import save_last_run_date, load_last_run_date
from bs4_scrape import scrapelibs, scrapedate
from datetime import datetime
from db_tools import write_to_alas_db, write_to_lib_db, del_existing, search_library_by_id
from smtp_module import send_email
import json



def parser(entry,update = 0):
    title_raw = entry.title
    link = entry.link
    cve = entry.description
    #convert to datetime.
    raw_pubdate = entry.published
    pubdate = datetime.strptime(raw_pubdate, "%a, %d %b %Y %H:%M:%S GMT")
    
    raw_updated = entry.updated
    updated = datetime.strptime(raw_updated, "%a, %d %b %Y %H:%M:%S GMT")
    #extracting the title details
    # print(title_raw)
    id, severity, component = title_details(title_raw)
    # print("parser title details debug", id, severity, component)
    #calling bs4_scrape to scrape the patch and updated date 
    patch = scrapelibs(link)
    # print("pubdate:", pubdate)
    # print("updated:", updated)
    # print("patch", patch)
    # print("main_parse.py test id sev, component", id, severity, component)
    if update == 1:
        del_existing('alas.db',id)
        del_existing('alas_lib.db',id)
        print("Existing entries with the following ID are deleted: ",id)
    #(id, title, severity, component, cve, pubdate, updated, link))
    write_to_alas_db(id, title_raw, severity, component, cve, pubdate, updated, link)
    for entry in patch:
        write_to_lib_db(entry, id)
        # print("test entry", entry)
    return id

def filter_id_components(ids, components, severity, dates):
    #loading from JSON
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        matching_data = []
        for i in range(len(components)):
            if components[i] in config["watchlist"]:
                matching_data.append((ids[i], components[i], severity[i], dates[i]))
        return matching_data

def update_parser(url):
    # print("update parser run",url)
    count = 0
    updated_ids = []
    updated_components = []
    updated_severity = []
    updated_dates = []
    # print("testing",url)
    #parse RSS feed
    feed = feedparser.parse(url)
    #load last run date from file
    last_run_date = load_last_run_date()
    print("update parser last run date",last_run_date)
    for entry in feed.entries:
        raw_updated = entry.updated
        # print("raw_updated in update parser", raw_updated)
        updated = datetime.strptime(raw_updated, "%a, %d %b %Y %H:%M:%S GMT")
        print("ALAS last updated", updated, last_run_date, updated > last_run_date)
        if updated > last_run_date:
            print("Updated entry found:", entry.title)
            #remove entries by using parser() with option = 1
            newid = parser(entry,1)
            updated_ids.append(newid)
            count += 1
    print ("Total updated entries:", count) 
    print ("Updated IDs:", updated_ids)
    
    ##debug updated IDs, to remove:
    # updated_ids = ['ALAS-2023-1855', 'ALAS-2023-1854', 'ALAS-2023-1853', 'ALAS-2011-8']
    # updated_ids = []
    if updated_ids:   
        for entry in updated_ids:
            # print("test entry", entry)
            result = search_library_by_id(entry)

            severity, component, cve, pubdate, updated_date, link = result[0]
            updated_severity.append(severity)
            updated_components.append(component)
            updated_dates.append(updated_date)
            # print(result)
            # print(component)
        ## sending email using updated_ids (full)
        email_text = 0
        email_text = "This is a full table of updates\nID, component etc\n"
        for i in range(len(updated_ids)):
            email_text += f"{updated_ids[i]}, {updated_components[i]}, {updated_severity[i]}, {updated_dates[i]}\n"
        send_email(email_text)

        #filter only watchlist
        filtered = filter_id_components(updated_ids, updated_components, updated_severity, updated_dates)
        print(filtered)
        #send email using filtered
        filtered_email_text = "This is a filtered table of updates\nID, component etc\n"
        for i in range(len(filtered)):
            filtered_email_text+= f"{filtered[i]}\n"
        send_email(filtered_email_text)
    else:
        print("No updates found, no email sent")

    save_last_run_date()



# def title_details_old(title):
#     #suggested pattern to split: <title>ALAS-2023-2285 (important): python-reportlab</title>
#     pattern = r'ALAS-(\d+-\d+) \((\w+)\): (.+)'
#     match = re.match(pattern, title)
#     if match:
#         #testing
#         # print(f'ALAS-{match.group(1)}')
#         # print(match.group(2))
#         # print(match.group(3))
#         #regex to only identify ALAS-type alerts. Returned statement for ID to follow full ALAS notation. 
#         return f'ALAS-{match.group(1)}', match.group(2), match.group(3)
#     else:
#         #testing
#         print("no match")
#         return None, None, None

def title_details(title):
    # print("title_details title", title)
    # Updated pattern to handle titles with version information: <title>ALASLIVEPATCH-2023-155 (important): kernel-livepatch-5.10.186-179.751</title>
    # Updated pattern to accept anything between spaces: <title>ALASLIVEPATCH-2023-155 (important): kernel-livepatch-5.10.186-179.751</title>
    # Split the title into parts using spaces and parentheses
    parts = re.split(r'[\s():]+', title)
    # print("parts", parts)
    # print("len parts", len(parts))
    if len(parts) >= 3 and parts[0].startswith('ALAS'):
        # Extracting relevant information
        identifier = parts[0]
        severity = parts[1]
        # severity = parts[2]
        libraries = ' '.join(parts[2:])
        return identifier, severity, libraries
        # return f'{identifier}-{date}', severity, version
    else:
        print("no match")
        print("title_details troubleshoot", title, parts)
        return None, None, None




def main():
    print("testing")
    #url = 'https://alas.aws.amazon.com/AL2/alas.rss'
    #local path for testing
    # url= 'alas.aws.amazon.com_alas_20231014.rss'
    url = "https://alas.aws.amazon.com/AL2/ALASLIVEPATCH-2023-155.html"
    # title_details(url)
    #short RSS for dev
    
    # url = 'alas_test_updated.rss'
    update_parser(url)
    pass




if __name__ == '__main__':
    main()



