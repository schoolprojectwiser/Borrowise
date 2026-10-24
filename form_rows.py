# ==========================================================
# form_rows.py
# Reusable "label + input" rows used by the Borrow and Return
# forms (entry, fixed/read-only, date, combo, spinbox).
# ==========================================================

import tkinter as tk
from tkinter import ttk


class FormRowsMixin:
    """Builders for one labelled form row each."""

    def _row_label(self, row, label_text):
        # MAIN COMMENT: Adds the bold left-hand label of a form row.
        tk.Label(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF",
            width=22,
            anchor="w",
        ).pack(side="left")

    def _row_box(self, row):
        # MAIN COMMENT: Adds the white bordered box that holds the input.
        box = tk.Frame(
            row,
            bg="white",
            highlightbackground=self.line_color,
            highlightcolor=self.line_color,
            highlightthickness=2,
        )
        box.pack(side="left", fill="x", expand=True)
        return box

    def create_fixed_status_row(self, parent, label_text, status_value):
        # MAIN COMMENT: Row with a READ-ONLY (disabled) entry showing a
        # value the user cannot change (auto ID, today's date, status).
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        self._row_label(row, label_text)
        entry_container = self._row_box(row)

        entry = tk.Entry(
            entry_container,
            font=("Arial", 13),
            fg=self.text_blue,
            bg="white",
            relief="flat",
            bd=0,
        )
        entry.pack(fill="x", padx=10, pady=10)
        entry.insert(0, status_value)
        entry.config(state="disabled")  # lock it

        return entry

    def create_date_row(self, parent, label_text, default_value, allow_past=False):
        # MAIN COMMENT: Row with a date entry (digits and "-" only) and a
        # calendar button that opens the date picker popup.
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        self._row_label(row, label_text)
        entry_container = self._row_box(row)

        entry = tk.Entry(
            entry_container,
            font=("Arial", 13),
            fg=self.text_blue,
            bg="white",
            relief="flat",
            bd=0,
            validate="key",
            validatecommand=self.vcmd_date,
        )
        entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        entry.insert(0, default_value)

        # Calendar button on the right of the entry
        tk.Button(
            entry_container,
            text="📅",
            font=("Segoe UI Emoji", 13),
            fg=self.text_blue,
            bg="white",
            activebackground="#E8F4FF",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.open_calendar(entry, allow_past),
        ).pack(side="right", padx=(0, 8))

        return entry

    def create_entry_row(self, parent, label_text, placeholder):
        # MAIN COMMENT: Row with a normal text entry that shows placeholder
        # text until the user clicks it.
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        self._row_label(row, label_text)
        entry_container = self._row_box(row)

        entry = tk.Entry(
            entry_container,
            font=("Arial", 13),
            fg="#47789E",
            bg="white",
            relief="flat",
            bd=0,
        )
        entry.pack(fill="x", padx=10, pady=10)

        entry.insert(0, placeholder)
        entry.bind(
            "<FocusIn>",
            lambda event, e=entry, p=placeholder: self.clear_placeholder(e, p),
        )

        return entry

    def clear_placeholder(self, entry, placeholder):
        # MAIN COMMENT: Removes the placeholder text from an entry the
        # first time the user focuses it.
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.text_blue)

    def create_combo_row(self, parent, label_text, values):
        # MAIN COMMENT: Row with a read-only dropdown (first value selected).
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        self._row_label(row, label_text)
        combo_container = self._row_box(row)

        combo = ttk.Combobox(
            combo_container,
            values=values,
            state="readonly",
            style="Borrowise.TCombobox",
        )
        combo.pack(fill="x", padx=2, pady=2)
        combo.current(0)

        return combo

    def create_spinbox_row(self, parent, label_text):
        # MAIN COMMENT: Row with a number spinbox (1 to 20) for quantity.
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        self._row_label(row, label_text)
        spin_container = self._row_box(row)

        spinbox = tk.Spinbox(
            spin_container,
            from_=1,
            to=20,
            font=("Arial", 13),
            relief="flat",
            bd=0,
            bg="white",
            fg=self.text_blue,
        )
        spinbox.pack(fill="x", padx=10, pady=8)

        return spinbox
