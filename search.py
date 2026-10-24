# ==========================================================
# search.py
# Search Records page: search by a chosen field and show the
# matching records in a table.
# ==========================================================

import tkinter as tk
from tkinter import ttk


class SearchMixin:
    """Search feature."""

    def show_search(self):
        # MAIN COMMENT: Draws the Search page: "Search by" dropdown, keyword
        # box, Search button and the results table (starts with all records).
        self.clear_content()

        self.page_title("Search Records", "Search for borrowed or returned items.")

        # ----- search bar card -----
        search_container = self.create_container(self.content_frame)
        search_container.pack(fill="x", padx=45, pady=(5, 15))

        search_frame = tk.Frame(search_container, bg="#F8FCFF")
        search_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(
            search_frame, text="Search by:", font=("Arial", 12, "bold"),
            fg=self.text_blue, bg="#F8FCFF",
        ).pack(side="left", padx=(0, 10))

        # Field selector
        self.search_combo = ttk.Combobox(
            search_frame,
            values=[
                "ID Number", "Name", "Item", "Quantity",
                "Status", "Borrow Date", "Return Date",
            ],
            state="readonly",
            style="Borrowise.TCombobox",
            width=15,
        )
        self.search_combo.current(0)
        self.search_combo.pack(side="left", padx=(0, 10))

        # Keyword entry
        search_input_container = tk.Frame(
            search_frame, bg="#FFFFFF",
            highlightbackground=self.line_color, highlightthickness=2,
        )
        search_input_container.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.search_entry = tk.Entry(
            search_input_container, font=("Arial", 12), bg="#FFFFFF",
            fg="#8AA2BD", relief="flat", bd=0,
        )
        self.search_entry.pack(fill="x", padx=10, pady=10)
        self.search_entry.insert(0, "Enter keyword...")
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)
        self.search_entry.bind("<Return>", lambda event: self.search_records())

        # Search button
        tk.Button(
            search_frame, text="🔍Search", font=("Arial", 12, "bold"),
            fg="#FFFFFF", bg=self.blue, activebackground="#087DDC",
            activeforeground="#FFFFFF", relief="flat", bd=0, padx=22, pady=10,
            cursor="hand2", command=self.search_records,
        ).pack(side="left")

        # ----- results table -----
        results_container = self.create_container(self.content_frame)
        results_container.pack(fill="both", expand=True, padx=45, pady=(0, 25))

        self.create_bordered_table(results_container, "search")
        self.display_search_results(self.records)

    def clear_search_placeholder(self, event):
        # MAIN COMMENT: Removes the "Enter keyword..." placeholder when the
        # user clicks the search box.
        if self.search_entry.get() == "Enter keyword...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=self.text_blue)

    def search_records(self):
        # MAIN COMMENT: Filters the records by the chosen field and keyword
        # (case-insensitive, partial match). Empty keyword shows everything.

        keyword = self.search_entry.get().strip().lower()

        # Placeholder text means "no keyword"
        if keyword == "enter keyword...":
            keyword = ""

        if not keyword:
            self.display_search_results(self.records)
            return

        # Translate the dropdown text into the record's dictionary key
        search_type = self.search_combo.get()
        field_mapping = {
            "ID Number": "borrower_id",
            "Name": "name",
            "Item": "item",
            "Quantity": "quantity",
            "Status": "status",
            "Borrow Date": "borrow_date",
            "Return Date": "return_date",
        }

        field = field_mapping.get(search_type)
        if field is None:
            self.display_search_results([])
            return

        # Collect the matching records
        results = []
        for record in self.records:
            value = str(record.get(field, "")).strip().lower()
            if keyword in value:
                results.append(record)

        self.display_search_results(results)

    def display_search_results(self, results):
        # MAIN COMMENT: Shows the given records in the search results table
        # (does nothing if the Search page is not open).
        if not hasattr(self, "search_table_frame"):
            return

        self.populate_bordered_table(self.search_table_frame, results)
