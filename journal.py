import sys, json
import tkinter as tk
from datetime import datetime

fileread = "journal.json"
filewrite = "journal.txt"

def load_data():
    with open(fileread, "r") as file:
        data = json.load(file)
        return(data)
    
def save_data(data):
    with open(fileread, "r+") as file:
        data = json.dump(data, file, indent=4)

def add_thru_terminal(data):
    date = get_valid_date()
    print("[i] Write your journal entry. Press Ctrl+D (or Ctrl+Z on Windows) when done:\n")
    entry = sys.stdin.read().strip()

    try:
        with open(fileread, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[date] = entry

    with open(fileread, "w") as f:
        json.dump(data, f, indent=2)
    return data

def add_thru_text_box(data):
    date = get_valid_date()
    def save_entry():
        content = text.get("1.0", tk.END).strip()
        if not content:
            root.destroy()
            return

        try:
            with open(fileread, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[date] = content

        with open(fileread, "w") as f:
            json.dump(data, f, indent=2)

        root.destroy()
        return data

    root = tk.Tk()
    root.title("Journal Entry")

    text = tk.Text(root, wrap='word', height=20, width=60)
    text.pack(padx=10, pady=10)

    save_button = tk.Button(root, text="Save Entry", command=save_entry)
    save_button.pack(pady=(0, 10))

    root.mainloop()
    try:
        with open(fileread, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def edit_entry(data):
    date = get_valid_date()
    try:
        with open(fileread, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[x] No journal file found.")
        return

    if date not in data:
        print(f"[x] No entry found for {date}")
        return

    print(f"{date}:\n\n{data[date]}")
    print("\n[i] Write your new version. Press Ctrl+D (or Ctrl+Z on Windows) when done:\n")
    new_entry = sys.stdin.read().strip()

    if new_entry:
        data[date] = new_entry
        with open(fileread, "w") as f:
            json.dump(data, f, indent=2)
        print("[i] Entry updated.")
    else:
        print("[x] No changes made.")
    return data

def remove_entry():
    try:
        with open(fileread, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[x] No journal file found.")
        return

    date = get_valid_date()
    if date in data:
        confirm = input(f"[!] Are you sure you want to delete the entry for {date}? (y/n): ").lower()
        if confirm == 'y':
            del data[date]
            with open(fileread, "w") as f:
                json.dump(data, f, indent=2)
            print("[i] Entry removed.")
        else:
            print("[x] Cancelled.")
    else:
        print("[x] No entry found for that date.")

    with open(fileread, "w") as f:
        json.dump(data, f, indent=2)
    return data

def view_entry(data):
    date = get_valid_date()
    if date in data:
        print(f"\n{date}:\n{data[date]}")
    else:
        print(f"\n[x] No entry for '{date}'!")

def get_valid_date(prompt="date [YYYY-MM-DD]: "):
    while True:
        date_input = input(prompt).strip()
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("[!] Invalid date format! Please use YYYY-MM-DD.")

def export_to_file(data):
    if not data:
        print("[x] No journal entries to export.")
        return

    try:
        with open(filewrite, "w") as file:
            for date, entry in data.items():
                file.write(f"{date}:\n{entry}\n\n")
        print(f"\n[i] Diary entries exported to {filewrite} successfully!")
    except Exception as e:
        print(f"[x] Error exporting entries: {e}")

def main():
    data = load_data()
    while True:
        print("\nJOURNAL MENU")
        print("- - - - -")
        print("\n  [1] Add thru terminal")
        print("  [2] Add thru text box")
        print("\n  [3] Edit")
        print("  [4] Remove")
        print("  [5] View")
        print("\n  [6] Export to File")
        print("  [7] Quit")
        choice = input("\n> ").strip()
        if choice == "1":
            data = add_thru_terminal(data)
        elif choice == "2":
            data = add_thru_text_box(data)
        elif choice == "3":
            data = edit_entry(data)
        elif choice == "4":
            data = remove_entry()
        elif choice == "5":
            view_entry(data)
        elif choice == "6":
            export_to_file(data)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("[!] Invalid option! Please try again.")

main()