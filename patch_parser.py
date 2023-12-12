

import re
import csv

def extract_cves_from_logs(log_file):
    entry_pattern = re.compile(r"(.+?)\.(\S+?)\s+\|\s+CHANGED\s+\|\s+rc=0\s+>>\s+\n.*CVE-(\d{4}-\d{4,7})\s+(\S+)\s+(.+?)\s*$")
    extracted_entries = []
    with open(log_file, "r") as file:
        log_content = file.read()
        matches = entry_pattern.findall(log_content)
        for match in matches:
            location, any_text, cve, rating, package = match
            extracted_entries.append((f"{location}.{any_text}".strip(), f"CVE-{cve}", rating.strip(), package.strip()))
            print(package)
    return extracted_entries

def generate_csv(entries, output_file="output.csv"):
    with open(output_file, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Location", "CVE", "Rating", "Package"])
        for entry in entries:
            csv_writer.writerow(entry)


def main():
    log_file = "prd_patchstatus_20231006101717.txt"
    extracted_entries = extract_cves_from_logs(log_file)
    generate_csv(extracted_entries)
    print("completed")

if __name__ == "__main__":
    main()



