# ==========================================================
# theme.py
# Colors and ttk styles (Treeview, Combobox) of the app.
# ==========================================================

from tkinter import ttk


class ThemeMixin:
    """Color palette and ttk style setup."""

    def init_colors(self):
        # MAIN COMMENT: Stores every color of the app as attributes of the
        # app object so any screen can use them (self.blue, self.dark_blue...).

        self.bg_color = "#F5FAFF"

        self.dark_blue = "#123F87"
        self.blue = "#1677E8"
        self.medium_blue = "#4B96E8"

        self.light_blue = "#9CCCF5"
        self.lighter_blue = "#E8F4FF"

        self.border_blue = "#C8DDF2"
        self.text_gray = "#60799B"
        self.text_blue = "#123F87"

        self.sidebar_color = "#063B73"
        self.green = "#27B96F"
        self.purple = "#7655E8"
        self.orange = "#F5A623"

        self.white = "#FFFFFF"
        self.line_color = "#B9DDF5"

    def init_styles(self):
        # MAIN COMMENT: Configures the ttk styles used by the Treeview
        # and the custom Borrowise combobox.

        style = ttk.Style()

        # "clam" allows custom colors on most platforms
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # ----- Treeview -----
        style.configure(
            "Borrowise.Treeview",
            background="#F8FCFF",
            fieldbackground="#F8FCFF",
            foreground="#123F87",
            font=("Arial", 12),
            rowheight=42,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Borrowise.Treeview.Heading",
            background="#DDF1FC",
            foreground="#123F87",
            font=("Arial", 12, "bold"),
            padding=12,
            relief="flat",
        )
        style.map(
            "Borrowise.Treeview",
            background=[("selected", "#B9DDF5")],
            foreground=[("selected", "#123F87")],
        )
        style.map(
            "Borrowise.Treeview.Heading",
            background=[("active", "#C8E5FA")],
        )

        # ----- Combobox -----
        style.configure(
            "Borrowise.TCombobox",
            fieldbackground="#FFFFFF",
            background="#FFFFFF",
            foreground="#123F87",
            arrowcolor="#557AA7",
            borderwidth=0,
            padding=4,
        )
        style.map(
            "Borrowise.TCombobox",
            fieldbackground=[("readonly", "#FFFFFF")],
            foreground=[("readonly", "#123F87")],
            selectbackground=[("readonly", "#FFFFFF")],
            selectforeground=[("readonly", "#123F87")],
        )

        # Font of the dropdown list of every combobox
        self.root.option_add("*TCombobox*Listbox.font", ("Arial", 12))
