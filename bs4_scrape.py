# import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz

#note: scrapedate can be deprecated as updated = entry.updated works.
def scrapedate(url):
    #timezone converter since web page is pacific and RSS is UTC
    pacific_tz = pytz.timezone('America/Los_Angeles')
    utc_tz = pytz.timezone('UTC')
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    date_text = 0
    alas_info_spans = soup.find_all("span", class_="alas-info")

    for alas_info_span in alas_info_spans:
        text = alas_info_span.text
        if "Advisory Updated Date" in text:
            #reset date_text
            date_text = 0
            
            date_string = text.split('Advisory Updated Date: ')[1].split(' Pacific')[0]

            # Parse the date string into a datetime object
            # updated_date_str = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
            
            updated_date_pacific = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
            updated_date_pacific = pacific_tz.localize(updated_date_pacific)

            # Convert to UTC
            updated_date_utc = updated_date_pacific.astimezone(utc_tz)

            #replace date_text:
            date_text = updated_date_utc
            print('Date found')
            break
    #debug
    # print(date_text)
    #output is datetime
    return date_text


def oldscrapelibs(url):
    response = requests.get(url)
    new_packages = 0
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        new_packages_div = soup.find('div', {'id': 'new_packages'})
        
        if new_packages_div:
            new_packages = []
            for package in new_packages_div.find_all('pre'):
                package_lines = package.text.strip().split('\n')
                print("debug package line")
                print(package_lines)
                for line in package_lines:
                    # Remove unwanted strings like '&nbsp;' and non-breaking space characters
                    cleaned_line = line.replace('&nbsp;', '').replace('\xa0', '').strip()
                    # for line2 in cleaned_line1:
                    #     # Remove unwanted strings like '&nbsp;' and non-breaking space characters
                    #     cleaned_line2 = line2.strip()
                    #     # Remove unwanted strings like 'aarch64:' and 'noarch:' as these are headers to the various sections and not wanted
                    filter_keywords = ["aarch64:", "noarch:", "src:", "x86_64:"]
                    entries = [entry.strip() for entry in cleaned_line.split() if entry.strip() and entry.strip(":") not in filter_keywords]

                    
                    print("debug line")
                    print(line)
                    print(entries)
                    if cleaned_line:
                        new_packages.append(cleaned_line)
            
            # Print or use the new_packages list as needed
            print('New package found:')
            print(new_packages)
        else:
            print('New Packages not found on the page.')
    else:
        print('Failed to retrieve the webpage.')

    return new_packages


def scrapelibs(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the <div> with id 'new_packages'
    new_packages_div = soup.find('div', {'id': 'new_packages'})
    # Find all <br /> elements within the 'New Packages' section (these are the dividers)
    # sample:  <div id='new_packages'> <b>New Packages:</b><pre>noarch:<br />&nbsp;&nbsp;&nbsp; python3-wheel-wheel-0.37.1-1.amzn2023.0.3.noarch<br /> etc
    br_elements = new_packages_div.find_all('br')

    #  Remove unwanted strings like 'aarch64:' and 'noarch:' as these are headers to the various sections and not wanted
    filter_keywords = ["aarch64:", "noarch:", "src:", "x86_64:","i686:"]

    # Extract and split the text from <br /> elements
    new_packages_entries = []
    for br in br_elements:
        # Get the previous sibling of <br />
        previous_sibling = br.previous_sibling
        # Check if the previous sibling is not None and not a NavigableString
        if previous_sibling and not callable(previous_sibling):
            # Extract text and strip spaces
            entry = previous_sibling.strip()
            # Check if the entry is not empty
            if entry and all(keyword not in entry for keyword in filter_keywords):
                new_packages_entries.append(entry)
    #debug
    # print(new_packages_entries)
    #output is [lib, lib, lib,...] as string
    return new_packages_entries


def main():
    print('test')
    url = 'https://alas.aws.amazon.com/AL2023/ALAS-2023-264.html'

    date = scrapedate(url)
    libraries = scrapelibs(url)
    print("processing done")
    print(date)
    print(libraries)
    print('end')
    pass



if __name__ == '__main__':
    main()


