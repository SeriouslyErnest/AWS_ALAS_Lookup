import sqlite3
import csv
import tkinter as tk
from tkinter import ttk
from db_tools import search_library_by_id

# def search_library_by_id(library_id): <- moved to DB tools
#     connection = sqlite3.connect("alas.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT severity, component, cve, pubdate, updated, link FROM alas WHERE id=?", (library_id,))
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
        csvwriter.writerow(['Library', 'ID', 'Severity', 'Component', 'CVE', 'Pubdate', 'Updated', 'Link'])
        csvwriter.writerows(data)

def search_library():
    query = entry.get().replace(",", " ").split() 
    query = [term.strip().lower() for term in query] 
    conn = sqlite3.connect('alas_lib.db')
    c = conn.cursor()
    # Clear previous search results
    tree.delete(*tree.get_children())  
    
    
    c.execute('''SELECT library, id FROM alas''')
    libraries = c.fetchall()
    unmatched_items = query.copy()

    for library, library_id in libraries:
        library_name = library.lower()
        # Check if any search term partially matches the library name
        if any(term in library_name for term in query):
            # Get details of the library by ID
            library_details = search_library_by_id(library_id)
            if library_details:
                # Extract details
                severity, component, cve, pubdate, updated, link = library_details[0]
                tree.insert('', 'end', values=(library, library_id, severity, component, cve, pubdate, updated, link))
                # Remove matched terms from unmatched_items
                unmatched_items = [term for term in unmatched_items if term not in library_name]

    # Add remaining unmatched items with "No ID" to the tree
    for library in unmatched_items:
        tree.insert('', 'end', values=(library, "No ID", "", "", "", "", "", ""))

    # Display error message if no results found
    if not tree.get_children():
        error_label.config(text="No results found.")

    # Close database connection
    conn.close()
    
    #old code doesn't handle multiple entries
    # query = entry.get().replace(",", " ").split()  # Split input by spaces and ignore commas
    # query = [term.strip().lower() for term in query]  # Remove spaces around terms and convert to lowercase
    # # Connect to the database
    # conn = sqlite3.connect('alas_lib.db')
    # c = conn.cursor()

    # tree.delete(*tree.get_children())  # Clear previous search results

    # # Search for libraries in the database
    # c.execute('''SELECT library, id FROM alas''')
    # libraries = c.fetchall()

    # unmatched_items = query.copy()
    # selected_items = []


    # for library, library_id in libraries:
    #     library_name = library.lower()
    #     matched_terms = [term for term in unmatched_items if term in library_name]
    #     if matched_terms and library_id:
    #         # Get details of the library by ID
    #         library_details = search_library_by_id(library_id)
    #         if library_details:
    #             # Extract details
    #             severity, component, cve, pubdate, updated, link = library_details[0]
    #             selected_items.append((library, library_id, severity, component, cve, pubdate, updated, link))
    #             # Remove matched terms from unmatched_items
    #             #note: since system searches for "in", partial entries will only show the first result meaning .x86 or .src will only have one. This logic is ok since all are in the same ALAS.
    #             unmatched_items = [term for term in unmatched_items if term not in matched_terms]

    # # Add matched items to the tree
    # for item in selected_items:
    #     tree.insert('', 'end', values=item)

    # # Add remaining unmatched items with "No ID" to the tree
    # print("unmatched", unmatched_items)
    # for library in unmatched_items:
    #     tree.insert('', 'end', values=(library, "No ID", "", "", "", "", "", ""))

    # # Display error message if no results found
    # if not tree.get_children():
    #     error_label.config(text="No results found.")

    # # Close database connection
    # conn.close()



def lib_search_ui():
    global root, entry, tree, error_label
    root = tk.Tk()
    root.title("Library Search")

    # Entry for user input
    entry_label = tk.Label(root, text="Enter libraries (separated by space or comma):")
    entry_label.pack()
    entry = tk.Entry(root, width=50)
    entry.pack()

    # Treeview for displaying search results
    tree = ttk.Treeview(root, columns=('Library', 'ID', 'Severity', 'Component', 'CVE', 'Pubdate', 'Updated', 'Link'), show='headings')
    tree.heading('Library', text='Library')
    tree.heading('ID', text='ID')
    tree.heading('Severity', text='Severity')
    tree.heading('Component', text='Component')
    tree.heading('CVE', text='CVE')
    tree.heading('Pubdate', text='Pubdate')
    tree.heading('Updated', text='Updated')
    tree.heading('Link', text='Link')
    tree.pack()

    # Search button
    search_button = tk.Button(root, text="Search", command=search_library)
    search_button.pack()

    # Button for saving results to CSV
    save_button = tk.Button(root, text="Save to CSV", command=lambda: save_to_csv(tree))
    save_button.pack()

    # Error message label
    error_label = tk.Label(root, fg="red")
    error_label.pack()

    root.mainloop()

def main():
    lib_search_ui()
    pass


if __name__ == "__main__":
    main()