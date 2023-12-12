#adapted from libsearch
import sqlite3
import csv
import tkinter as tk
from tkinter import ttk
from db_tools import search_library_by_id

# def search_library_by_id(search_id):
#     connection = sqlite3.connect("alas.db")
#     cursor = connection.cursor()

#     # Use SQL query to find exact ID match
#     cursor.execute("SELECT severity, component, cve, pubdate, updated, link FROM alas WHERE id=?", (search_id,))
#     results = cursor.fetchall()
#     connection.close()

#     return results

def save_to_csv(tree):
    items = tree.get_children()
    data = []
    for item in items:
        values = tree.item(item, 'values')
        data.append(values)
    with open('search_results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Severity', 'Component', 'CVE', 'Pubdate', 'Updated', 'Link'])
        csvwriter.writerows(data)

def search_id():
    query = entry.get().replace(",", " ").split()  # Split input by spaces and ignore commas
    query = [term.strip().upper() for term in query]  # Remove spaces around terms and convert to uppercase

    tree.delete(*tree.get_children())  # Clear previous search results

    unmatched_items = query.copy()
    selected_items = []

    for search_id in query:
        # Get details of the library by ID
        library_details = search_library_by_id(search_id)
        if library_details:
            # Extract details
            severity, component, cve, pubdate, updated, link = library_details[0]
            selected_items.append((search_id, severity, component, cve, pubdate, updated, link))
            unmatched_items.remove(search_id)

    # Add matched items to the tree
    for item in selected_items:
        tree.insert('', 'end', values=item)

    # Add remaining unmatched items with "No ID" to the tree
    for search_id in unmatched_items:
        tree.insert('', 'end', values=(search_id, "No result", "", "", "", "", ""))

    # Display error message if no results found
    if not tree.get_children():
        error_label.config(text="No results found.")

def id_search_ui():
    global root, entry, tree, error_label
    root = tk.Tk()
    root.title("ALAS-ID Search")

    # Entry for user input
    entry_label = tk.Label(root, text="Enter ALAS IDs (separated by space or comma):")
    entry_label.pack()
    entry = tk.Entry(root, width=50)
    entry.pack()

    # Treeview for displaying search results
    tree = ttk.Treeview(root, columns=('ID', 'Severity', 'Component', 'CVE', 'Pubdate', 'Updated', 'Link'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Severity', text='Severity')
    tree.heading('Component', text='Component')
    tree.heading('CVE', text='CVE')
    tree.heading('Pubdate', text='Pubdate')
    tree.heading('Updated', text='Updated')
    tree.heading('Link', text='Link')
    tree.pack()

    # Search button
    search_button = tk.Button(root, text="Search", command=search_id)
    search_button.pack()

    # Button for saving results to CSV
    save_button = tk.Button(root, text="Save to CSV", command=lambda: save_to_csv(tree))
    save_button.pack()

    # Error message label
    error_label = tk.Label(root, fg="red")
    error_label.pack()

    root.mainloop()

def main():
    id_search_ui()

if __name__ == "__main__":
    main()
