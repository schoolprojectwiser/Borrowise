# ==========================================================
# login.py
# Login screen: logo, ID Number + password form, buttons and
# the first login step (ID + password check).
# ==========================================================

import time
import tkinter as tk

from password_entry import PasswordEntry


class LoginMixin:
    """Login screen and credential check."""

    def show_login(self):
        # MAIN COMMENT: Clears the window and builds the login screen
        # (canvas background, logo and form).
        for widget in self.root.winfo_children():
            widget.destroy()

        self.background = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            bg=self.bg_color,
            highlightthickness=0,
        )
        self.background.place(x=0, y=0)
        self.center_x = self.screen_width // 2

        self.create_logo()
        self.create_login_form()

    def create_logo(self):
        # MAIN COMMENT: Draws the 3D box logo and the "Borrowise / SURPLUS"
        # title on the login canvas.
        cx = self.center_x
        cy = 150

        # top face of the box
        self.background.create_polygon(
            cx, cy - 40, cx + 45, cy - 15, cx, cy + 12, cx - 45, cy - 15,
            fill="#F5FAFF", outline="#1555A5", width=3,
        )
        # left face
        self.background.create_polygon(
            cx - 45, cy - 15, cx, cy + 12, cx, cy + 62, cx - 45, cy + 35,
            fill="#BFE1FA", outline="#1555A5", width=3,
        )
        # right face
        self.background.create_polygon(
            cx, cy + 12, cx + 45, cy - 15, cx + 45, cy + 35, cx, cy + 62,
            fill="#8CC9F1", outline="#1555A5", width=3,
        )
        # app name + subtitle
        self.background.create_text(
            self.center_x, 240, text="Borrowise",
            font=("Arial", 38, "bold"), fill="#0E3B82",
        )
        self.background.create_text(
            self.center_x, 277, text="SURPLUS",
            font=("Arial", 15, "bold"), fill="#5A78A0",
        )

    def make_login_frame(self, y):
        # MAIN COMMENT: Creates one white bordered input box of the login
        # form at the given vertical position.
        frame = tk.Frame(
            self.root,
            bg="#FFFFFF",
            highlightbackground=self.border_blue,
            highlightthickness=2,
        )
        frame.place(x=self.center_x, y=y, width=420, height=54, anchor="center")
        return frame

    def create_login_form(self):
        # MAIN COMMENT: Builds the ID Number field, password field, LOGIN
        # button, "Forgot password?" and "Create new account" buttons.

        # ----- ID Number -----
        self.id_frame = self.make_login_frame(335)
        self.create_card_icon(self.id_frame, 35, 27)

        self.id_entry = tk.Entry(
            self.id_frame,
            font=("Arial", 14),
            fg=self.text_gray,
            bg="#FFFFFF",
            bd=0,
            relief="flat",
            validate="key",
            validatecommand=self.vcmd_id,
        )
        self.id_entry.place(x=70, y=13, width=330, height=28)
        self.id_entry.insert(0, "ID Number")
        self.bind_placeholder(self.id_entry, "ID Number", "#123F87", self.text_gray)

        # ----- Password (with eye icon) -----
        self.password_frame = self.make_login_frame(405)
        self.create_lock_icon(self.password_frame, 35, 27)

        self.password_field = PasswordEntry(
            self.password_frame,
            placeholder="Password",
            bg="#FFFFFF",
            fg="#123F87",
            placeholder_fg=self.text_gray,
            font=("Arial", 14),
        )
        self.password_field.place(x=62, y=9, width=345, height=34)

        # ----- LOGIN button -----
        self.login_button = tk.Button(
            self.root,
            text="LOGIN",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#1269D0",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.login,
        )
        self.login_button.place(
            x=self.center_x, y=480, width=420, height=54, anchor="center"
        )

        # Enter key also logs in
        self.root.bind("<Return>", lambda event: self.login())

        # ----- Forgot password -----
        self.forgot_password = tk.Button(
            self.root,
            text="Forgot password?",
            font=("Arial", 11, "bold"),
            fg="black",
            bg=self.bg_color,
            activeforeground="black",
            activebackground=self.bg_color,
            bd=0,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
            command=self.open_forgot_password_window,
        )
        self.forgot_password.place(x=self.center_x, y=540, anchor="center")

        # ----- Create new account -----
        self.create_account = tk.Button(
            self.root,
            text="Create new account",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#39FF14",
            activeforeground="white",
            activebackground="#32E612",
            bd=0,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
            padx=25,
            pady=8,
            command=self.open_create_account_window,
        )
        self.create_account.place(x=self.center_x, y=590, anchor="center")

    def login(self):
        # MAIN COMMENT: Step 1 of login. Checks the ID Number and password.
        # If correct -> opens the SECURITY ANSWER popup (step 2).
        # If wrong -> counts a failed attempt and starts the lockout.

        # Block login while the lockout timer is running
        if time.time() < self.lockout_until:
            self.show_lockout_popup()
            return

        id_num = self.id_entry.get().strip()
        password = self.password_field.get()

        # Treat the placeholder text as empty
        if id_num == "ID Number":
            id_num = ""

        account = self.registered_accounts.get(id_num)

        authenticated = bool(account and account["password"] == password)

        if authenticated:
            # ID + password OK -> now ask the security question
            self.show_security_answer_popup(id_num, account)
            return

        self.register_failed_attempt("Incorrect ID Number or password.")
