# ==========================================================
# profile.py
# Profile page: account details + borrowing summary cards.
# ==========================================================

import tkinter as tk


class ProfileMixin:
    """Profile page."""

    def show_profile(self):
        # MAIN COMMENT: Draws the Profile page: avatar, name, ID Number,
        # read-only account details and the borrowing summary.
        self.clear_content()

        self.page_title("My Profile", "View and manage your account information.")

        # ----- top card (avatar + details) -----
        profile_card = tk.Frame(
            self.content_frame, bg="#F8FCFF",
            highlightbackground="#DDF1FC", highlightthickness=2,
        )
        profile_card.pack(fill="x", padx=45, pady=(0, 25), ipady=15)

        left_profile = tk.Frame(profile_card, bg="#F8FCFF")
        left_profile.pack(side="left", padx=40, pady=20)

        # Simple drawn avatar (circle + head + shoulders)
        avatar_canvas = tk.Canvas(
            left_profile, width=110, height=110, bg="#F8FCFF", highlightthickness=0
        )
        avatar_canvas.pack(side="left")
        avatar_canvas.create_oval(5, 5, 105, 105, fill="#D8EBFA", outline="")
        avatar_canvas.create_oval(40, 25, 70, 55, fill="#0E3B82", outline="")
        avatar_canvas.create_arc(
            20, 58, 90, 115, start=0, extent=180, fill="#0E3B82", outline=""
        )

        # Name and ID Number
        user_info_frame = tk.Frame(left_profile, bg="#F8FCFF")
        user_info_frame.pack(side="left", padx=20)

        name_str = self.current_user.get("fullname", "USER").upper()
        id_str = self.current_user.get("id", "ID Number")

        tk.Label(
            user_info_frame, text=name_str, font=("Arial", 28, "bold"),
            fg="#0E3B82", bg="#F8FCFF",
        ).pack(anchor="w")

        tk.Label(
            user_info_frame, text=f"ID Number: {id_str}", font=("Arial", 14),
            fg="#6689A8", bg="#F8FCFF",
        ).pack(anchor="w", pady=(2, 0))

        # Vertical divider
        divider = tk.Frame(profile_card, bg="#B9DDF5", width=2)
        divider.pack(side="left", fill="y", pady=20)

        # ----- account details (read-only entries) -----
        right_details = tk.Frame(profile_card, bg="#F8FCFF")
        right_details.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        header_frame = tk.Frame(right_details, bg="#F8FCFF")
        header_frame.pack(anchor="w", pady=(0, 15))

        tk.Label(
            header_frame, text="🪪", font=("Segoe UI Emoji", 14), bg="#F8FCFF"
        ).pack(side="left", padx=(0, 5))

        tk.Label(
            header_frame, text="ACCOUNT DETAILS", font=("Arial", 14, "bold"),
            fg="#0E3B82", bg="#F8FCFF",
        ).pack(side="left")

        fields = [
            ("ID Number :", self.current_user.get("id", "")),
            ("Full Name :", self.current_user.get("fullname", "")),
        ]

        for label_text, val in fields:
            row_f = tk.Frame(right_details, bg="#F8FCFF")
            row_f.pack(fill="x", pady=4)

            tk.Label(
                row_f, text=label_text, font=("Arial", 12, "bold"),
                fg="#123F87", bg="#F8FCFF", width=18, anchor="w",
            ).pack(side="left")

            entry_box = tk.Entry(
                row_f, font=("Arial", 11), fg="#123F87", bg="#F2F8FD",
                relief="solid", bd=1,
            )
            entry_box.pack(side="left", fill="x", expand=True, ipady=4, padx=5)
            entry_box.insert(0, val)
            entry_box.config(state="readonly")

        # ----- summary card -----
        summary_card = tk.Frame(
            self.content_frame, bg="#F8FCFF",
            highlightbackground="#DDF1FC", highlightthickness=2,
        )
        summary_card.pack(fill="both", expand=True, padx=45, pady=(0, 25), ipady=15)

        sum_header = tk.Frame(summary_card, bg="#F8FCFF")
        sum_header.pack(fill="x", padx=25, pady=(15, 5))

        tk.Label(
            sum_header, text="📊 Borrowise Summary", font=("Arial", 16, "bold"),
            fg="#0E3B82", bg="#F8FCFF",
        ).pack(anchor="w")

        tk.Label(
            sum_header, text="Quick overview of your borrowing activity.",
            font=("Arial", 11), fg="#6689A8", bg="#F8FCFF",
        ).pack(anchor="w")

        sum_cards_frame = tk.Frame(summary_card, bg="#F8FCFF")
        sum_cards_frame.pack(fill="x", padx=25, pady=15)

        for col in range(3):
            sum_cards_frame.grid_columnconfigure(col, weight=1, uniform="sum_cards")

        # Count the records by status
        borrowed_count = sum(1 for r in self.records if r.get("status") == "Borrowed")
        returned_count = sum(1 for r in self.records if r.get("status") == "Returned")
        overdue_count = sum(1 for r in self.records if r.get("status") in ["Lost", "Damaged"])

        # Card 1: currently borrowed
        c1 = tk.Frame(sum_cards_frame, bg="#EBF5FC", highlightbackground="#3A9AD9", highlightthickness=1)
        c1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(c1, text="📦", font=("Segoe UI Emoji", 20), bg="#EBF5FC").pack(side="left", padx=15, pady=15)
        c1_text = tk.Frame(c1, bg="#EBF5FC")
        c1_text.pack(side="left", pady=10)
        tk.Label(c1_text, text="Currently Borrowed", font=("Arial", 11, "bold"), fg="#123F87", bg="#EBF5FC").pack(anchor="w")
        tk.Label(c1_text, text=str(borrowed_count), font=("Arial", 22, "bold"), fg="#123F87", bg="#EBF5FC").pack(anchor="w")
        tk.Label(c1_text, text="Items", font=("Arial", 9), fg="#6689A8", bg="#EBF5FC").pack(anchor="w")

        # Card 2: returned
        c2 = tk.Frame(sum_cards_frame, bg="#EBF8F2", highlightbackground="#27B96F", highlightthickness=1)
        c2.grid(row=0, column=1, sticky="nsew", padx=5)
        tk.Label(c2, text="🔄", font=("Segoe UI Emoji", 20), bg="#EBF8F2").pack(side="left", padx=15, pady=15)
        c2_text = tk.Frame(c2, bg="#EBF8F2")
        c2_text.pack(side="left", pady=10)
        tk.Label(c2_text, text="Return Items", font=("Arial", 11, "bold"), fg="#197D49", bg="#EBF8F2").pack(anchor="w")
        tk.Label(c2_text, text=str(returned_count), font=("Arial", 22, "bold"), fg="#197D49", bg="#EBF8F2").pack(anchor="w")
        tk.Label(c2_text, text="Items", font=("Arial", 9), fg="#5EA680", bg="#EBF8F2").pack(anchor="w")

        # Card 3: lost / damaged
        c3 = tk.Frame(sum_cards_frame, bg="#FDEAEA", highlightbackground="#E74C3C", highlightthickness=1)
        c3.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        tk.Label(c3, text="⚠️", font=("Segoe UI Emoji", 20), bg="#FDEAEA").pack(side="left", padx=15, pady=15)
        c3_text = tk.Frame(c3, bg="#FDEAEA")
        c3_text.pack(side="left", pady=10)
        tk.Label(c3_text, text="Overdue Items", font=("Arial", 11, "bold"), fg="#A93226", bg="#FDEAEA").pack(anchor="w")
        tk.Label(c3_text, text=str(overdue_count), font=("Arial", 22, "bold"), fg="#A93226", bg="#FDEAEA").pack(anchor="w")
        tk.Label(c3_text, text="Item" if overdue_count == 1 else "Items", font=("Arial", 9), fg="#C07870", bg="#FDEAEA").pack(anchor="w")
