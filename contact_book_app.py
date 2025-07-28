
# code for contact book formation 

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


DATA_FILE = "contacts.json"

def read_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def write_contacts(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def insert_new():
    person = {
        "name": name_input.get().strip(),
        "phone": phone_input.get().strip(),
        "email": email_input.get().strip(),
        "address": addr_input.get().strip()
    }

    if not person["name"] or not person["phone"]:
        messagebox.showwarning("Missing Info", "Name and phone no. are required.")
        return

    existing = read_contacts()
    existing.append(person)
    write_contacts(existing)
    refresh_display()
    messagebox.showinfo("Added", f"{person['name']} added successfully.")
    reset_inputs()

def refresh_display():
    listbox.delete(0, tk.END)
    data = read_contacts()
    for entry in data:
        listbox.insert(tk.END, f"{entry['name']} - {entry['phone']}")

def remove_selected():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a contact to remove.")
        return

    selected_name = listbox.get(selected[0]).split(" - ")[0]
    data = read_contacts()
    updated = [c for c in data if c["name"] != selected_name]

    write_contacts(updated)
    refresh_display()
    messagebox.showinfo("Deleted", f"Deleted {selected_name}")

def edit_selected():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Choose a contact to update.")
        return

    target_name = listbox.get(selected[0]).split(" - ")[0]
    contacts = read_contacts()

    for idx, entry in enumerate(contacts):
        if entry["name"] == target_name:
            updated_name = simpledialog.askstring("Edit Name", "New Name:", initialvalue=entry["name"])
            updated_phone = simpledialog.askstring("Edit Phone", "New Phone:", initialvalue=entry["phone"])
            updated_email = simpledialog.askstring("Edit Email", "New Email:", initialvalue=entry["email"])
            updated_address = simpledialog.askstring("Edit Address", "New Address:", initialvalue=entry["address"])

            if updated_name and updated_phone:
                contacts[idx] = {
                    "name": updated_name,
                    "phone": updated_phone,
                    "email": updated_email,
                    "address": updated_address
                }
                write_contacts(contacts)
                refresh_display()
                messagebox.showinfo("Updated", f"{updated_name} updated successfully.")
                return
            else:
                messagebox.showwarning("Error", "Name and phone must not be empty.")
                return

def find_contact():
    keyword = simpledialog.askstring("Search Contact", "Type name to search:")
    if not keyword:
        return

    filtered = []
    data = read_contacts()
    for entry in data:
        if keyword.lower() in entry["name"].lower():
            filtered.append(f"{entry['name']} - {entry['phone']}")

    listbox.delete(0, tk.END)
    if filtered:
        for item in filtered:
            listbox.insert(tk.END, item)
    else:
        messagebox.showinfo("No Match", f"No contact matching '{keyword}' found.")

def reset_inputs():
    name_input.delete(0, tk.END)
    phone_input.delete(0, tk.END)
    email_input.delete(0, tk.END)
    addr_input.delete(0, tk.END)

# ---------- UI Setup ----------
app = tk.Tk()
app.title("CONTACT-BOOK 📘")
app.geometry("500x540")
app.config(bg="#1A859B")  # Soft pink background

#  now we'll apply the color and styles to make it better
label_bg = "#494748"
entry_bg = "#fff7fb"
listbox_bg = "#f0f8ff"
btn_color = "#444a4a"
btn_active = "#7aaed0"
btn_fg = "white"
entry_width = 40

# Input fields is here
tk.Label(app, text="Full Name", bg=label_bg).pack()
name_input = tk.Entry(app, width=entry_width, bg=entry_bg)
name_input.pack()

tk.Label(app, text="Phone Number", bg=label_bg).pack()
phone_input = tk.Entry(app, width=entry_width, bg=entry_bg)
phone_input.pack()

tk.Label(app, text="Email ID", bg=label_bg).pack()
email_input = tk.Entry(app, width=entry_width, bg=entry_bg)
email_input.pack()

tk.Label(app, text="Home Address", bg=label_bg).pack()
addr_input = tk.Entry(app, width=entry_width, bg=entry_bg)
addr_input.pack()

# Buttons works id here
controls = tk.Frame(app, bg=label_bg)
controls.pack(pady=12)

button_style = {
    "width": 10,
    "bg": btn_color,
    "fg": btn_fg,
    "activebackground": btn_active,
    "activeforeground": "white",
    "bd": 0,
    "font": ("Segoe UI", 9, "bold"),
    "padx": 2,
    "pady": 2
}

tk.Button(controls, text="Add", command=insert_new, **button_style).grid(row=0, column=0, padx=5)
tk.Button(controls, text="Show All", command=refresh_display, **button_style).grid(row=0, column=1, padx=5)
tk.Button(controls, text="Search", command=find_contact, **button_style).grid(row=0, column=2, padx=5)
tk.Button(controls, text="Update", command=edit_selected, **button_style).grid(row=1, column=0, pady=5)
tk.Button(controls, text="Delete", command=remove_selected, **button_style).grid(row=1, column=1, pady=5)
tk.Button(controls, text="Clear", command=reset_inputs, **button_style).grid(row=1, column=2, pady=5)

# Listbox for contact display
tk.Label(app, text="Saved Contacts", bg=label_bg).pack()
listbox = tk.Listbox(app, width=60, height=10, bg=listbox_bg, fg="black", bd=0, highlightthickness=1)
listbox.pack(pady=10)

refresh_display()
app.mainloop()
