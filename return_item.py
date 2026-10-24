# ==========================================================
# return_item.py
# Return Item page: mark a borrowed item as Returned, Lost
# or Damaged.
# ==========================================================

import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from config import DATE_FORMAT


class ReturnItemMixin:
    """Return Item feature."""

    def show_return(self):
        # MAIN COMMENT: Draws the Return Item page: form fields, the three
        # status buttons (Returned / Lost / Damaged) and a reminder box.
        self.clear_content()

        self.page_title("📦 Return Item", "Enter the details of the borrowed item.")

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        form = tk.Frame(container, bg="#F8FCFF")
        form.pack(fill="x", padx=25, pady=25)

        # Fields the user types to find the borrowed record
        self.return_id_entry = self.create_entry_row(form, "ID Number:", "Enter ID number")
        self.return_name_entry = self.create_entry_row(form, "Borrower Name:", "Enter name")
        self.return_item_entry = self.create_entry_row(form, "Item:", "Enter item")

        # Return date is today's date and locked (automatic)
        today = datetime.now().strftime(DATE_FORMAT)
        self.return_date_entry = self.create_fixed_status_row(form, "Return Date:", today)

        # ----- status buttons -----
        return_btn_frame = tk.Frame(form, bg="#F8FCFF")
        return_btn_frame.pack(pady=20)

        tk.Button(
            return_btn_frame, text="📦 Mark as Returned", font=("Arial", 12, "bold"),
            fg="white", bg=self.green, activebackground="#1FA762",
            relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
            command=lambda: self.process_item_status("Returned"),
        ).pack(side="left", padx=5)

        tk.Button(
            return_btn_frame, text="⚠️ Mark as Lost", font=("Arial", 12, "bold"),
            fg="white", bg=self.orange, activebackground="#D98E1B",
            relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
            command=lambda: self.process_item_status("Lost"),
        ).pack(side="left", padx=5)

        tk.Button(
            return_btn_frame, text="❌ Mark as Damaged", font=("Arial", 12, "bold"),
            fg="white", bg="#E74C3C", activebackground="#C0392B",
            relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
            command=lambda: self.process_item_status("Damaged"),
        ).pack(side="left", padx=5)

        # ----- reminder box -----
        info_frame = tk.Frame(form, bg="#E8F6FD")
        info_frame.pack(fill="x", pady=(5, 5), padx=5)

        tk.Label(
            info_frame, text="ⓘ", font=("Arial", 20, "bold"),
            fg=self.blue, bg="#E8F6FD",
        ).pack(side="left", padx=(15, 10), pady=12)

        tk.Label(
            info_frame,
            text='Return Reminder\nPlease return the borrowed item within 3 weeks. Make sure to update its status on or before the expected return date.',
            font=("Arial", 9), fg=self.text_blue, bg="#E8F6FD", justify="left",
        ).pack(side="left", pady=12)

    def process_item_status(self, new_status):
        # MAIN COMMENT: Finds the matching "Borrowed" record (ID, name and
        # item must match) and changes its status to Returned/Lost/Damaged.

        borrower_id = self.return_id_entry.get().strip()
        name = self.return_name_entry.get().strip()
        item = self.return_item_entry.get().strip()

        # Return date is set automatically to today
        return_date = datetime.now().strftime(DATE_FORMAT)

        # Required fields
        if borrower_id == "" or borrower_id == "Enter ID number":
            messagebox.showwarning("Borrowise", "Please enter the ID number.")
            return

        if name == "" or name == "Enter name":
            messagebox.showwarning("Borrowise", "Please enter the borrower name.")
            return

        if item == "" or item == "Enter item":
            messagebox.showwarning("Borrowise", "Please enter the item.")
            return

        # Look for the first active (still "Borrowed") record that matches
        found = False
        for record in self.records:
            if (
                record["borrower_id"].lower() == borrower_id.lower()
                and record["name"].lower() == name.lower()
                and record["item"].lower() == item.lower()
                and record["status"] == "Borrowed"
            ):
                record["status"] = new_status
                record["return_date"] = return_date
                found = True
                break

        if found:
            messagebox.showinfo(
                "Borrowise",
                f"Item status has been successfully updated to '{new_status}'.",
            )
            self.show_records()
        else:
            messagebox.showwarning(
                "Borrowise", "No matching active borrowed item was found."
            )
