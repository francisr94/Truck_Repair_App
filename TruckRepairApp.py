import tkinter as tk
from tkinter import messagebox
import sqlite3


class TruckRepairApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Truck Repair Shop Parts Management")
        self.parts_index_map = {}
        # Create database or connect to existing one
        self.conn = sqlite3.connect('truck_repair.db')
        self.c = self.conn.cursor()
        self.create_table()

        # Parts Entry Frame
        self.parts_frame = tk.LabelFrame(self.master, text="Parts")
        pads_value = 20  # Example value, replace it with your desired value
        pad_value = 10  # Example value, replace it with your desired value
        self.parts_frame.pack(fill="both", expand="yes", padx=pads_value, pady=pad_value)

        # Part Name Entry
        self.part_name_label = tk.Label(self.parts_frame, text="Part Name:")
        self.part_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.part_name_entry = tk.Entry(self.parts_frame)
        self.part_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Part Quantity Entry
        self.part_qty_label = tk.Label(self.parts_frame, text="Quantity:")
        self.part_qty_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.part_qty_entry = tk.Entry(self.parts_frame)
        self.part_qty_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Add Part Button
        self.add_part_button = tk.Button(self.parts_frame, text="Add Part", command=self.add_part)
        self.add_part_button.grid(row=2, columnspan=2, padx=5, pady=5)

        # Parts List Frame
        self.parts_list_frame = tk.LabelFrame(self.master, text="Parts List")
        self.parts_list_frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Parts Listbox
        self.parts_listbox = tk.Listbox(self.parts_list_frame, width=50)
        self.parts_listbox.pack(padx=5, pady=5)

        # Fetch parts from database
        self.show_parts()

        # Delete Part Button
        self.delete_part_button = tk.Button(self.parts_list_frame, text="Delete Part", command=self.delete_part)
        self.delete_part_button.pack(padx=5, pady=5)

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS parts
                         (id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         quantity INTEGER NOT NULL)''')
        self.conn.commit()

    def add_part(self):
        part_name = self.part_name_entry.get()
        part_qty = self.part_qty_entry.get()

        if part_name and part_qty:
            try:
                part_qty = int(part_qty)
                if part_qty < 0:
                    messagebox.showerror("Error", "Quantity cannot be negative.")
                    return
                self.c.execute("INSERT INTO parts (name, quantity) VALUES (?, ?)", (part_name, part_qty))
                self.conn.commit()
                self.part_name_entry.delete(0, tk.END)
                self.part_qty_entry.delete(0, tk.END)
                self.show_parts()  # Update parts list after adding a new part
                messagebox.showinfo("Success", "Part added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a valid integer.")
        else:
            messagebox.showerror("Error", "Please enter both part name and quantity.")

    def show_parts(self):
        self.parts_listbox.delete(0, tk.END)
        self.parts_index_map.clear()  # Clear the mapping dictionary
        self.c.execute("SELECT * FROM parts")
        parts = self.c.fetchall()
        for index, part in enumerate(parts):
            part_id = part[0]
            part_name = part[1]
            part_qty = part[2]
            self.parts_index_map[part_id] = index  # Map part ID to listbox index
            self.parts_listbox.insert(tk.END, f"{part_id}: {part_name} - {part_qty}")

    def delete_part(self):
        selected_index = self.parts_listbox.curselection()
        if selected_index:
            selected_item = self.parts_listbox.get(selected_index[0])
            try:
                # Extract part ID from the selected item
                part_id_str = selected_item.split(':')[0].strip()
                part_id = int(part_id_str)
                self.c.execute("DELETE FROM parts WHERE id=?", (part_id,))
                self.conn.commit()
                self.show_parts()
                messagebox.showinfo("Success", "Part deleted successfully!")
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Failed to extract or convert part ID.")
        else:
            messagebox.showerror("Error", "Please select a part to delete.")


def main():
    root = tk.Tk()
    TruckRepairApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
