import sqlite3
import csv
import tkinter as tk
from tkinter import ttk
from db_tools import search_library_by_id

partial_match = True  # Initial setting for partial match

def toggle_partial_match():
    global partial_match
    partial_match = not partial_match
    partial_match_label.config(text=f"Partial Match: {'On' if partial_match else 'Off'}")

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

    tree.delete(*tree.get_children())

    c.execute('''SELECT library, id FROM alas''')
    libraries = c.fetchall()

    for term in query:
        unmatched_items = [term]
        selected_items = []

        for library, library_id in libraries:
            library_name = library.lower()

            if (partial_match and term in library_name) or (not partial_match and term == library_name):
                library_details = search_library_by_id(library_id)
                if library_details:
                    severity, component, cve, pubdate, updated, link = library_details[0]
                    selected_items.append((library, library_id, severity, component, cve, pubdate, updated, link))
                    unmatched_items = [t for t in unmatched_items if t != term]

        for item in selected_items:
            tree.insert('', 'end', values=item)

        if unmatched_items:
            tree.insert('', 'end', values=(unmatched_items[0], "No ID", "", "", "", "", "", ""))

    if not tree.get_children():
        error_label.config(text="No results found.")

    conn.close()

def lib_search_ui():
    global root, entry, tree, error_label, partial_match_label
    root = tk.Tk()
    root.title("Library Search")

    entry_label = tk.Label(root, text="Enter libraries (separated by space or comma):")
    entry_label.pack()
    entry = tk.Entry(root, width=50)
    entry.pack()

    partial_match_button = tk.Button(root, text="Toggle Partial Match", command=toggle_partial_match)
    partial_match_button.pack()

    partial_match_label = tk.Label(root, text=f"Partial Match: {'On' if partial_match else 'Off'}")
    partial_match_label.pack()

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

    search_button = tk.Button(root, text="Search", command=search_library)
    search_button.pack()

    save_button = tk.Button(root, text="Save to CSV", command=lambda: save_to_csv(tree))
    save_button.pack()

    error_label = tk.Label(root, fg="red")
    error_label.pack()

    root.mainloop()

def main():
    lib_search_ui()

if __name__ == "__main__":
    main()
