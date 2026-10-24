# ==========================================================
# records.py
# Borrowing Records page and the bordered table widget that
# is also reused by the Search page.
# ==========================================================

import tkinter as tk
from tkinter import ttk


class RecordsMixin:
    """Records page + reusable table."""

    # Column titles shown in the table (and in downloaded files)
    TABLE_COLUMNS = (
        "ID Number",
        "Name",
        "Item",
        "Quantity",
        "Borrow Date",
        "Return Date",
        "Status",
    )

    # Dictionary keys of a record, in the same order as TABLE_COLUMNS
    TABLE_KEYS = (
        "borrower_id",
        "name",
        "item",
        "quantity",
        "borrow_date",
        "return_date",
        "status",
    )

    def show_records(self):
        # MAIN COMMENT: Draws the Borrowing Records page: title with a
        # Download button and the table of every record.
        self.clear_content()

        self.page_title(
            "Borrowing Records",
            "View all borrowed and returned items.",
            action=self.create_download_button,
        )

        container = self.create_container(self.content_frame)
        container.pack(fill="both", expand=True, padx=45, pady=(5, 25))

        self.create_bordered_table(container, "records")
        self.populate_bordered_table(self.records_table_frame, self.records)

    def create_download_button(self, parent):
        # MAIN COMMENT: Creates the "Download" dropdown button (PDF / JPG)
        # shown at the top-right of the Records page.
        menubutton = tk.Menubutton(
            parent,
            text="⬇ Download ▾",
            font=("Arial", 13, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#087DDC",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
        )

        menu = tk.Menu(menubutton, tearoff=0, font=("Arial", 11))
        menu.add_command(
            label="Download as PDF", command=lambda: self.download_records("pdf")
        )
        menu.add_command(
            label="Download as JPG", command=lambda: self.download_records("jpg")
        )
        menubutton.config(menu=menu)

        return menubutton

    def create_bordered_table(self, parent, table_name):
        # MAIN COMMENT: Creates an empty scrollable, centered table area and
        # saves it as self.<table_name>_table_frame (e.g. records_table_frame).
        table_container = tk.Frame(parent, bg="#F8FCFF")
        table_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Canvas + scrollbar make the table scrollable
        canvas = tk.Canvas(table_container, bg="#F8FCFF", highlightthickness=0)
        vertical_scrollbar = ttk.Scrollbar(
            table_container, orient="vertical", command=canvas.yview
        )
        canvas.configure(yscrollcommand=vertical_scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Frame inside the canvas that holds the real cells
        table_frame = tk.Frame(canvas, bg="#C8DDF2")
        canvas_window = canvas.create_window((0, 0), window=table_frame, anchor="nw")

        def center_table(event=None):
            # Keeps the table centered and updates the scroll area
            canvas_width = canvas.winfo_width()
            table_width = table_frame.winfo_reqwidth()
            table_height = table_frame.winfo_reqheight()

            x = max((canvas_width - table_width) // 2, 0)
            canvas.coords(canvas_window, x, 0)
            canvas.configure(
                scrollregion=(0, 0, max(canvas_width, table_width), table_height)
            )

        table_frame.bind("<Configure>", center_table)
        canvas.bind("<Configure>", center_table)

        # Save references with a name so Records and Search can each own one
        setattr(self, f"{table_name}_table_canvas", canvas)
        setattr(self, f"{table_name}_table_frame", table_frame)
        setattr(self, f"{table_name}_table_window", canvas_window)

        return table_frame

    def populate_bordered_table(self, table_frame, records):
        # MAIN COMMENT: Fills a table frame with the heading row and one row
        # per record. Shows "No borrowing records available." when empty.

        columns = self.TABLE_COLUMNS

        # Width (in characters) of each column
        column_widths = {
            "ID Number": 18,
            "Name": 18,
            "Item": 15,
            "Quantity": 15,
            "Borrow Date": 13,
            "Return Date": 13,
            "Status": 12,
        }

        # Remove the old content first
        for widget in table_frame.winfo_children():
            widget.destroy()

        # ----- heading row -----
        for column_index, column in enumerate(columns):
            heading = tk.Label(
                table_frame,
                text=column,
                font=("Arial", 12, "bold"),
                fg="#123F87",
                bg="#DDF1FC",
                width=column_widths[column],
                height=2,
                relief="solid",
                bd=1,
                highlightbackground="#A8C5DF",
                highlightthickness=0.5,
                anchor="center",
            )
            heading.grid(row=0, column=column_index, sticky="nsew")

        # ----- empty message -----
        if not records:
            empty_label = tk.Label(
                table_frame,
                text="No borrowing records available.",
                font=("Arial", 11),
                fg=self.text_gray,
                bg="#F8FCFF",
                relief="solid",
                bd=1,
                padx=20,
                pady=15,
            )
            empty_label.grid(row=1, column=0, columnspan=len(columns), sticky="nsew")
            return

        # ----- data rows (alternating colors) -----
        for row_index, record in enumerate(records, start=1):
            values = tuple(record.get(key, "") for key in self.TABLE_KEYS)

            for column_index, value in enumerate(values):
                cell = tk.Label(
                    table_frame,
                    text=str(value),
                    font=("Arial", 11),
                    fg="#123F87",
                    bg="#FFFFFF" if row_index % 2 else "#F2F8FD",
                    width=column_widths[columns[column_index]],
                    height=2,
                    relief="solid",
                    bd=1,
                    highlightbackground="#C8DDF2",
                    highlightthickness=0.5,
                    anchor="center",
                )
                cell.grid(row=row_index, column=column_index, sticky="nsew")
