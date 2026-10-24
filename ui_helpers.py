# ==========================================================
# ui_helpers.py
# Small helpers shared by popups and page layouts:
# placeholders, popup centering, popup labels, page header...
# ==========================================================

import tkinter as tk
from tkinter import ttk

from config import QUESTION_PLACEHOLDER, SECURITY_QUESTIONS


class UIHelpersMixin:
    """Generic UI helper methods (no feature-specific logic)."""

    def bind_placeholder(self, entry, placeholder, normal_fg, placeholder_fg):
        # MAIN COMMENT: Gives an Entry placeholder behaviour: the text
        # disappears on focus and returns if the entry is left empty.

        def focus_in(event):
            # Remove placeholder when the user clicks the field
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=normal_fg)

        def focus_out(event):
            # Restore placeholder if nothing was typed
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg=placeholder_fg)

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)

    def center_popup(self, popup, width, height):
        # MAIN COMMENT: Sizes a popup window and places it in the middle
        # of the main window.
        popup.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - width // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - height // 2
        popup.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")

    def make_question_combo(self, parent, **kwargs):
        # MAIN COMMENT: Creates the read-only security-question dropdown
        # with the "Select security question" placeholder.
        combo = ttk.Combobox(
            parent,
            values=SECURITY_QUESTIONS,
            state="readonly",
            style="Borrowise.TCombobox",
            font=("Arial", 12),
            **kwargs
        )
        combo.set(QUESTION_PLACEHOLDER)
        # Remove the blue highlight after picking an item
        combo.bind("<<ComboboxSelected>>", lambda e: combo.selection_clear())
        return combo

    def popup_label(self, popup, text):
        # MAIN COMMENT: Adds a bold field label (left aligned) to a popup.
        tk.Label(
            popup,
            text=text,
            font=("Arial", 10, "bold"),
            fg=self.text_blue,
            bg="white",
        ).pack(anchor="w", padx=35)

    def popup_hint(self, popup, text, pady=(0, 8)):
        # MAIN COMMENT: Adds a small gray hint line (left aligned) to a popup.
        tk.Label(
            popup,
            text=text,
            font=("Arial", 10, "bold"),
            fg=self.text_gray,
            bg="white",
        ).pack(anchor="w", padx=35, pady=pady)

    def clear_content(self):
        # MAIN COMMENT: Removes everything from the right-hand content area
        # so a new page can be drawn.
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def page_title(self, title, subtitle, action=None):
        # MAIN COMMENT: Draws the big page title + subtitle. An optional
        # "action" function can add a widget (e.g. Download button) on the right.
        header = tk.Frame(self.content_frame, bg="#F2FAFF")
        header.pack(fill="x", padx=45, pady=(40, 25))

        left = tk.Frame(header, bg="#F2FAFF")
        left.pack(side="left")

        tk.Label(
            left, text=title, font=("Arial", 32, "bold"), fg="#123A8C", bg="#F2FAFF",
        ).pack(anchor="w", pady=(0, 3))

        tk.Label(
            left, text=subtitle, font=("Arial", 15), fg="#6689A8", bg="#F2FAFF",
        ).pack(anchor="w")

        # Optional widget on the right side of the header
        if action is not None:
            widget = action(header)
            widget.pack(side="right", anchor="n", pady=(8, 0))

    def create_container(self, parent):
        # MAIN COMMENT: Returns a light-blue bordered frame used as a card
        # around forms and tables (caller must pack it).
        container = tk.Frame(
            parent,
            bg="#F8FCFF",
            highlightbackground="#B9DDF5",
            highlightcolor="#B9DDF5",
            highlightthickness=2,
        )
        return container
