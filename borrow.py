# ==========================================================
# This the borrow.py
# Borrow Item page: form, validation, saving the record and
# the success popup.
# ==========================================================

import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from config import DATE_FORMAT, ITEM_CHOICES, ITEM_HEADERS, ITEM_PLACEHOLDER


class BorrowMixin:
    """Borrow Item feature."""

    def generate_next_borrower_id(self):
        # MAIN COMMENT: Builds the next automatic borrower ID, like
        # 01-01-2627-00001, based on how many records exist.
        prefix = "01-01-2627-"
        count = len(self.records) + 1
        return f"{prefix}{count:05d}"

    def show_borrow(self):
        # MAIN COMMENT: Draws the Borrow Item page with all form rows and the
        # Save / Clear buttons.
        self.clear_content()

        self.page_title("Borrow Item", "Enter the details of the item to be borrowed.")

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        form = tk.Frame(container, bg="#F8FCFF")
        form.pack(fill="x", padx=25, pady=25)

        # Auto-generated ID (locked)
        next_id = self.generate_next_borrower_id()
        self.borrower_id_entry = self.create_fixed_status_row(form, "ID Number:", next_id)

        # Borrower name
        self.borrower_entry = self.create_entry_row(form, "Borrower Name:", "Enter name")

        # Item dropdown (grouped by category)
        self.item_combo = self.create_combo_row(
            form, "Item Selection:", ITEM_CHOICES, height=16
        )
        self.last_item_choice = ITEM_PLACEHOLDER
        self.item_combo.bind("<<ComboboxSelected>>", self.on_item_selected)

        # Quantity
        self.quantity_spin = self.create_spinbox_row(form, "Quantity:")

        # Borrowing date = today (locked); expected return = pickable
        today = datetime.now().strftime(DATE_FORMAT)
        self.borrow_date_entry = self.create_fixed_status_row(form, "Borrowing Date:", today)
        self.expected_return_entry = self.create_date_row(form, "Expected Return Date:", today)

        # Status is always "Borrowed" for a new record (locked)
        self.status_entry = self.create_fixed_status_row(form, "Status:", "Borrowed")

        # ----- buttons -----
        button_frame = tk.Frame(form, bg="#F8FCFF")
        button_frame.pack(pady=(18, 5))

        tk.Button(
            button_frame, text="Save / Borrow", font=("Arial", 15, "bold"),
            fg="white", bg=self.blue, activebackground="#087DDC",
            relief="flat", bd=0, padx=45, pady=12, cursor="hand2",
            command=self.borrow_item,
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame, text="Clear", font=("Arial", 15, "bold"),
            fg=self.text_blue, bg="#DCEFFC", activebackground="#CBE9FA",
            relief="flat", bd=0, padx=45, pady=12, cursor="hand2",
            command=self.clear_borrow_form,
        ).pack(side="left", padx=8)

    def on_item_selected(self, event=None):
        # MAIN COMMENT: Category headers are only labels. If one is picked
        # (by click or mouse wheel), go back to the last real choice.
        chosen = self.item_combo.get()
        if chosen in ITEM_HEADERS:
            self.item_combo.set(self.last_item_choice)
        else:
            self.last_item_choice = chosen
        self.item_combo.selection_clear()

    def borrow_item(self):
        # MAIN COMMENT: Validates the Borrow form and, if everything is
        # correct, saves a new "Borrowed" record and shows the success popup.

        # Read the form values
        borrower_id = self.borrower_id_entry.get().strip()
        name = self.borrower_entry.get().strip()
        item = self.item_combo.get()
        quantity = self.quantity_spin.get().strip()
        borrow_date = self.borrow_date_entry.get().strip()
        return_date = self.expected_return_entry.get().strip()
        status = "Borrowed"

        # Required fields
        if borrower_id == "" or borrower_id == "Enter ID number":
            messagebox.showwarning("Borrowise", "Please enter the ID number.")
            return

        if name == "" or name == "Enter name":
            messagebox.showwarning("Borrowise", "Please enter the borrower name.")
            return

        if item == ITEM_PLACEHOLDER or item in ITEM_HEADERS:
            messagebox.showwarning("Borrowise", "Please select an item.")
            return

        # Quantity must be a whole number from 1 to 20
        try:
            qty = int(quantity)
        except ValueError:
            qty = 0
        if not 1 <= qty <= 20:
            messagebox.showwarning(
                "Borrowise", "Quantity must be a whole number from 1 to 20."
            )
            return
        quantity = str(qty)

        # Expected return date must be a real date
        try:
            expected = datetime.strptime(return_date, DATE_FORMAT).date()
        except ValueError:
            messagebox.showwarning(
                "Borrowise",
                "Please enter a valid Expected Return Date (MM-DD-YYYY),\n"
                "or pick one using the calendar button.",
            )
            return

        # Borrowing date (fallback to today if somehow invalid)
        try:
            borrowed_on = datetime.strptime(borrow_date, DATE_FORMAT).date()
        except ValueError:
            borrowed_on = datetime.now().date()

        # Return date cannot be before the borrowing date
        if expected < borrowed_on:
            messagebox.showwarning(
                "Borrowise",
                "The Expected Return Date cannot be earlier than the Borrowing Date.",
            )
            return

        # Save the record
        record = {
            "borrower_id": borrower_id,
            "name": name,
            "item": item,
            "quantity": quantity,
            "borrow_date": borrow_date,
            "return_date": return_date,
            "status": status,
        }

        self.records.append(record)
        self.save_data()
        self.show_success_popup()

    def clear_borrow_form(self):
        # MAIN COMMENT: Resets every field of the Borrow form to its
        # starting value (new auto ID, placeholder name, first item, today).

        # New auto ID (the entry is locked, so unlock -> change -> lock)
        self.borrower_id_entry.config(state="normal")
        self.borrower_id_entry.delete(0, tk.END)
        self.borrower_id_entry.insert(0, self.generate_next_borrower_id())
        self.borrower_id_entry.config(state="disabled")

        # Name back to placeholder
        self.borrower_entry.delete(0, tk.END)
        self.borrower_entry.insert(0, "Enter name")
        self.borrower_entry.config(fg="#47789E")

        # Item and quantity
        self.item_combo.current(0)
        self.last_item_choice = ITEM_PLACEHOLDER
        self.quantity_spin.delete(0, tk.END)
        self.quantity_spin.insert(0, "1")

        # Dates
        today = datetime.now().strftime(DATE_FORMAT)
        self.borrow_date_entry.config(state="normal")
        self.borrow_date_entry.delete(0, tk.END)
        self.borrow_date_entry.insert(0, today)
        self.borrow_date_entry.config(state="disabled")

        self.expected_return_entry.delete(0, tk.END)
        self.expected_return_entry.insert(0, today)

    def show_success_popup(self):
        # MAIN COMMENT: Shows the green "Success! Item has been borrowed"
        # popup; pressing OK closes it and clears the Borrow form.
        popup = tk.Toplevel(self.root)
        popup.title("Borrowise")
        popup.geometry("520x300")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        popup.grab_set()
        popup.update_idletasks()

        # Center on the main window
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 250
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - 100
        popup.geometry(f"500x300+{x}+{y}")

        body = tk.Frame(popup, bg="white")
        body.pack(fill="both", expand=True)

        tk.Label(
            body, text="✅", font=("Arial", 45, "bold"), fg="green"
        ).pack(side="left", padx=(40, 30), pady=35)

        text_frame = tk.Frame(body, bg="white")
        text_frame.pack(side="left", pady=35)

        tk.Label(
            text_frame, text="Success!", font=("Arial", 20, "bold"),
            fg=self.dark_blue, bg="white",
        ).pack(anchor="w")

        tk.Label(
            text_frame, text="Item has been borrowed successfully.",
            font=("Arial", 10), fg=self.text_blue, bg="white",
        ).pack(anchor="w", pady=(3, 20))

        def on_popup_close():
            # Close the popup and reset the form for the next borrower
            popup.destroy()
            self.clear_borrow_form()

        tk.Button(
            text_frame, text="OK", font=("Arial", 10, "bold"), fg="white",
            bg=self.blue, activebackground="#087DDC", relief="flat", bd=0,
            padx=65, pady=10, command=on_popup_close, cursor="hand2",
        ).pack(anchor="w")
