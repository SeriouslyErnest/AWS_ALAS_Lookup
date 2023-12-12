#this section pulls statistics from the ALAS database, giving information on how often the said library has which severities and when
# import sqlite3
import tkinter as tk
import datetime
import csv
from db_tools import search_entries_by_component_and_date

# def search_entries_by_component_and_date(component, date): <- consolidate in db_tools.py
#     connection = sqlite3.connect("alas.db")
#     cursor = connection.cursor()

#     # Use SQL query to find entries based on component and date
#     # Assuming 'pubdate' is stored as a string in the format 'YYYY-MM-DD HH:MM:SS'
#     cursor.execute("SELECT severity, substr(pubdate, 1, 10) FROM alas WHERE component=? AND substr(pubdate, 1, 10) > ?", (component, date))
#     results = cursor.fetchall()
#     connection.close()

#     return results

def search_entries():
    global component_entry, date_entry, entries, important_label, medium_label, low_label, error_label
    
    component = component_entry.get().strip()
    raw_date = date_entry.get().strip()

    try:
        # Parse the input date in 'YYYYMMDD' format
        input_date = datetime.datetime.strptime(raw_date, "%Y%m%d").date()

        # Format the input date back to 'YYYY-MM-DD' for database query
        formatted_date = input_date.strftime("%Y-%m-%d")
        
        # Search entries based on component and formatted date
        entries = search_entries_by_component_and_date(component, formatted_date)

        # Count severity types (ignore case)
        important_count = sum(1 for entry in entries if entry[0].lower() == 'important')
        medium_count = sum(1 for entry in entries if entry[0].lower() == 'medium')
        low_count = sum(1 for entry in entries if entry[0].lower() == 'low')

        # Update the labels with the counts
        important_label.config(text=f"Important: {important_count}")
        medium_label.config(text=f"Medium: {medium_count}")
        low_label.config(text=f"Low: {low_count}")

    except ValueError:
        error_label.config(text="Error: Invalid date format. Please use YYYYMMDD.")

    except Exception as e:
        # Handle other errors
        error_label.config(text=f"Error: {str(e)}")

def download_results(entries, component, entered_date):
    if entries:
        filename = f"{component}_entries_{entered_date}.csv"
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Severity', 'Date'])
            for entry in entries:
                severity, date = entry
                # Date from the database might include a time component; removing it
                date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                csvwriter.writerow([severity, date])
        error_label.config(text=f"Results downloaded as {filename}")
    else:
        error_label.config(text="No results to download.")

def lib_stats():
    global component_entry, date_entry, entries, important_label, medium_label, low_label, error_label
    
    root = tk.Tk()
    root.title("ALAS Search")

    # UI components
    component_label = tk.Label(root, text="Enter Component:")
    component_label.pack()
    component_entry = tk.Entry(root, width=50)
    component_entry.pack()

    date_label = tk.Label(root, text="Enter Date (YYYYMMDD):")
    date_label.pack()
    date_entry = tk.Entry(root, width=50)
    date_entry.pack()

    search_button = tk.Button(root, text="Search Entries", command=search_entries)
    search_button.pack()

    important_label = tk.Label(root, text="")
    important_label.pack()

    medium_label = tk.Label(root, text="")
    medium_label.pack()

    low_label = tk.Label(root, text="")
    low_label.pack()

    download_button = tk.Button(root, text="Download Results", command=lambda: download_results(entries, component_entry.get().strip(), date_entry.get().strip()))
    download_button.pack()

    error_label = tk.Label(root, fg="red")
    error_label.pack()

    root.mainloop()

def main():
    lib_stats()

if __name__ == "__main__":
    main()
