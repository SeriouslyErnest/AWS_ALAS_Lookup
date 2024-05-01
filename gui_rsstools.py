## this is the button to check and replace the URL used. 
import tkinter as tk
import json
import tkinter.messagebox as messagebox

def rss_tools():
    def check_rss_url():
        try:
            with open('config.json', 'r') as config_file:
                config_data = json.load(config_file)
                rss_url = config_data.get('rss_url', 'No URL found')
                messagebox.showinfo("RSS URL", f"Current URL: {rss_url}")
        except FileNotFoundError:
            messagebox.showerror("Error", "config.json not found")

    def update_rss_url():
        def save_url():
            new_url = url_entry.get()
            try:
                with open('config.json', 'r') as config_file:
                    config_data = json.load(config_file)
                config_data['rss_url'] = new_url
                with open('config.json', 'w') as config_file:
                    json.dump(config_data, config_file, indent=4)
                messagebox.showinfo("Success", "RSS URL updated successfully.\nIf you have updated the URL, redo the First Time Setup.")
                top.destroy()
            except FileNotFoundError:
                messagebox.showerror("Error", "config.json not found")

        top = tk.Toplevel(root)
        top.title("RSS URL Configuration")

        url_label = tk.Label(top, text="Enter new RSS URL:")
        url_label.pack()

        url_entry = tk.Entry(top, width=50)
        url_entry.pack()

        check_button = tk.Button(top, text="Check", command=check_rss_url)
        check_button.pack()

        save_button = tk.Button(top, text="Update URL", command=save_url)
        save_button.pack()

    # Create main window
    root = tk.Tk()
    root.title("ALAS Database Tool")

    # Button to open RSS URL configuration window
    rss_url_button = tk.Button(root, text="RSS URL", command=update_rss_url)
    rss_url_button.pack()

    root.mainloop()




def main():
    rss_tools()

if __name__ == "__main__":
    rss_tools()



