import sqlite3
from tkinter import *
from tkinter import messagebox

# Database setup
def initialize_db():
    with sqlite3.connect("contacts.db") as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL UNIQUE,
                        email TEXT,
                        address TEXT
                        )""")
        db.commit()

initialize_db()

# Contact Book Application
class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # Frames
        self.title_frame = Frame(self.root, bg="#4CAF50", pady=10)
        self.title_frame.pack(fill=X)

        self.form_frame = Frame(self.root, bg="#ffffff", pady=10)
        self.form_frame.pack(fill=X, padx=10)

        self.button_frame = Frame(self.root, bg="#f0f0f0", pady=10)
        self.button_frame.pack()

        self.list_frame = Frame(self.root, bg="#f0f0f0")
        self.list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.build_ui()

    def build_ui(self):
        # Title
        title_label = Label(self.title_frame, text="Contact Book", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white")
        title_label.pack()

        # Form Inputs
        Label(self.form_frame, text="Name", bg="#ffffff", anchor=W).grid(row=0, column=0, sticky=W, padx=10, pady=5)
        self.name_entry = Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.form_frame, text="Phone", bg="#ffffff", anchor=W).grid(row=1, column=0, sticky=W, padx=10, pady=5)
        self.phone_entry = Entry(self.form_frame)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.form_frame, text="Email", bg="#ffffff", anchor=W).grid(row=2, column=0, sticky=W, padx=10, pady=5)
        self.email_entry = Entry(self.form_frame)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.form_frame, text="Address", bg="#ffffff", anchor=W).grid(row=3, column=0, sticky=W, padx=10, pady=5)
        self.address_entry = Entry(self.form_frame)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        Button(self.button_frame, text="Add Contact", command=self.add_contact, bg="#4CAF50", fg="white", padx=10).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Update Contact", command=self.update_contact, bg="#FFC107", fg="white", padx=10).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Delete Contact", command=self.delete_contact, bg="#F44336", fg="white", padx=10).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Search Contact", command=self.search_contact, bg="#2196F3", fg="white", padx=10).pack(side=LEFT, padx=5)

        # Contact List
        self.contact_list = Listbox(self.list_frame, font=("Arial", 12), height=15, selectmode=SINGLE)
        self.contact_list.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.contact_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contact_list.yview)

        self.load_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required fields.")
            return

        try:
            with sqlite3.connect("contacts.db") as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
                db.commit()
                messagebox.showinfo("Success", "Contact added successfully.")
                self.clear_form()
                self.load_contacts()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Phone number already exists.")

    def update_contact(self):
        selected = self.contact_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "No contact selected.")
            return

        contact_id = self.contact_list.get(selected[0]).split()[0]
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required fields.")
            return

        with sqlite3.connect("contacts.db") as db:
            cursor = db.cursor()
            cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?", (name, phone, email, address, contact_id))
            db.commit()
            messagebox.showinfo("Success", "Contact updated successfully.")
            self.clear_form()
            self.load_contacts()

    def delete_contact(self):
        selected = self.contact_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "No contact selected.")
            return

        contact_id = self.contact_list.get(selected[0]).split()[0]

        with sqlite3.connect("contacts.db") as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            db.commit()
            messagebox.showinfo("Success", "Contact deleted successfully.")
            self.load_contacts()

    def search_contact(self):
        search_term = self.name_entry.get()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a name or phone number to search.")
            return

        with sqlite3.connect("contacts.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f"%{search_term}%", f"%{search_term}%"))
            rows = cursor.fetchall()

        self.contact_list.delete(0, END)
        for row in rows:
            self.contact_list.insert(END, f"{row[0]} {row[1]} ({row[2]})")

    def load_contacts(self):
        with sqlite3.connect("contacts.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM contacts")
            rows = cursor.fetchall()

        self.contact_list.delete(0, END)
        for row in rows:
            self.contact_list.insert(END, f"{row[0]} {row[1]} ({row[2]})")

    def clear_form(self):
        self.name_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.address_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = ContactBook(root)
    root.mainloop()
