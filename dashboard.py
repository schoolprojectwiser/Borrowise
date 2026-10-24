# ==========================================================
# dashboard.py
# Main window after login: sidebar + Home page with the four
# quick-action cards.
# ==========================================================

import tkinter as tk


class DashboardMixin:
    """Dashboard layout, sidebar and Home page."""

    def show_dashboard(self):
        # MAIN COMMENT: Replaces the login screen with the main layout
        # (sidebar on the left, content area on the right) and shows Home.
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self.root, bg="#F2FAFF")
        self.main_frame.pack(fill="both", expand=True)

        self.create_sidebar()

        self.content_frame = tk.Frame(self.main_frame, bg="#F2FAFF")
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.dashboard_home()

    def create_sidebar(self):
        # MAIN COMMENT: Builds the dark-blue sidebar: logo, navigation
        # buttons and the Profile button at the bottom.
        self.sidebar = tk.Frame(self.main_frame, bg="#063B73", width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ----- logo -----
        logo_frame = tk.Frame(self.sidebar, bg="#063B73")
        logo_frame.pack(fill="x", padx=25, pady=(35, 20))

        tk.Label(
            logo_frame, text="📦", font=("Segoe UI Emoji", 43),
            fg="#CBEAFF", bg="#063B73",
        ).pack(side="left")

        logo_text = tk.Frame(logo_frame, bg="#063B73")
        logo_text.pack(side="left", padx=10)

        tk.Label(
            logo_text, text="Borrowise", font=("Arial", 23, "bold"),
            fg="white", bg="#063B73",
        ).pack(anchor="w")

        tk.Label(
            logo_text, text="SURPLUS", font=("Arial", 13, "bold"),
            fg="#B9DDF5", bg="#063B73",
        ).pack(anchor="center", pady=(2, 0))

        # ----- navigation buttons -----
        nav_container = tk.Frame(self.sidebar, bg="#063B73")
        nav_container.pack(fill="both", expand=True)

        self.create_sidebar_button(nav_container, " 🏠", " Home", self.dashboard_home)
        self.create_sidebar_button(nav_container, " ➕", "Borrow Item", self.show_borrow)
        self.create_sidebar_button(nav_container, " 📦", "Return Item", self.show_return)
        self.create_sidebar_button(nav_container, " 📋", " Records", self.show_records)
        self.create_sidebar_button(nav_container, " 🔍", " Search", self.show_search)
        self.create_sidebar_button(nav_container, " ↪", " Logout", self.logout)

        # ----- profile button (bottom) -----
        profile_btn = tk.Button(
            self.sidebar,
            text=" 👤 Profile",
            command=self.show_profile,
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#0088FF",
            activebackground="#0077E6",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2",
        )
        profile_btn.pack(fill="x", padx=15, pady=(0, 25), side="bottom")

    def create_sidebar_button(self, parent, icon, text, command):
        # MAIN COMMENT: Creates one sidebar navigation button (icon + text)
        # that runs the given command when clicked.
        button = tk.Button(
            parent,
            text=f" {icon} {text}",
            command=command,
            font=("Arial", 15),
            fg="white",
            bg="#063B73",
            activebackground="#168CF5",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2",
        )
        button.pack(fill="x", padx=15, pady=3)

    def dashboard_home(self):
        # MAIN COMMENT: Draws the Home page: welcome text, four colored
        # action cards (Borrow, Return, Records, Search) and a quote banner.
        self.clear_content()

        tk.Label(
            self.content_frame, text="Welcome to Borrowise!",
            font=("Arial", 36, "bold"), fg="#123A8C", bg="#F2FAFF",
        ).pack(anchor="w", padx=45, pady=(40, 3))

        tk.Label(
            self.content_frame, text="Easily manage and monitor your borrowed items.",
            font=("Arial", 16), fg="#6689A8", bg="#F2FAFF",
        ).pack(anchor="w", padx=45, pady=(0, 28))

        # ----- 4 equal-width cards -----
        cards_frame = tk.Frame(self.content_frame, bg="#F2FAFF")
        cards_frame.pack(fill="x", padx=45)

        card_gap = 12
        for column in range(4):
            cards_frame.grid_columnconfigure(column, weight=1, uniform="dashboard_cards")

        borrow_card = self.create_dashboard_card(
            cards_frame, "➕", "Borrow\nItem", "#168CF5", self.show_borrow
        )
        borrow_card.grid(row=0, column=0, sticky="nsew", padx=(0, card_gap // 2))

        return_card = self.create_dashboard_card(
            cards_frame, "📦", "Return\nItem", "#27B96F", self.show_return
        )
        return_card.grid(row=0, column=1, sticky="nsew", padx=card_gap // 2)

        records_card = self.create_dashboard_card(
            cards_frame, "📋", "View\nRecords", "#7655E8", self.show_records
        )
        records_card.grid(row=0, column=2, sticky="nsew", padx=card_gap // 2)

        search_card = self.create_dashboard_card(
            cards_frame, "🔍", "Search\nRecords", "#F5A623", self.show_search
        )
        search_card.grid(row=0, column=3, sticky="nsew", padx=(card_gap // 2, 0))

        # ----- quote banner -----
        quote_container = tk.Frame(
            self.content_frame, bg="#E8F6FD",
            highlightbackground="#B9DDF5", highlightthickness=2,
        )
        quote_container.pack(fill="x", padx=45, pady=40, ipady=22)

        tk.Label(
            quote_container, text="📦", font=("Segoe UI Emoji", 38), bg="#E8F6FD"
        ).pack(side="left", padx=(35, 20))

        quote_text = tk.Frame(quote_container, bg="#E8F6FD")
        quote_text.pack(side="left")

        tk.Label(
            quote_text, text="“Borrowise smart. Keep track.”",
            font=("Arial", 19, "bold"), fg="#123A8C", bg="#E8F6FD",
        ).pack(anchor="w")

        tk.Label(
            quote_text, text="— Borrowise", font=("Arial", 13),
            fg="#6689A8", bg="#E8F6FD",
        ).pack(anchor="w", pady=(4, 0))

    def create_dashboard_card(self, parent, icon, text, color, command):
        # MAIN COMMENT: Creates one big clickable card (icon + text). Clicking
        # anywhere on the card runs the command.
        card = tk.Frame(parent, bg=color, height=205, cursor="hand2")
        card.pack_propagate(False)

        icon_label = tk.Label(
            card, text=icon, font=("Segoe UI Emoji", 40), fg="white", bg=color
        )
        icon_label.pack(pady=28)

        text_label = tk.Label(
            card, text=text, font=("Arial", 18, "bold"),
            fg="white", bg=color, justify="center",
        )
        text_label.pack()

        # The labels cover the frame, so bind the click on all three
        card.bind("<Button-1>", lambda event: command())
        icon_label.bind("<Button-1>", lambda event: command())
        text_label.bind("<Button-1>", lambda event: command())

        return card
