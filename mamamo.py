import calendar
import math
import os
import re
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

# ==========================================================
# SECURITY QUESTIONS / LOGIN SETTINGS
# ==========================================================

SECURITY_QUESTIONS = [
    "What is your pet name?",
    "What is your favorite food?",
    "What is your Mother's maiden name?",
    "What is your favorite color?",
    "What is your date of birth?",
]

QUESTION_PLACEHOLDER = "Select security question"

# Lockout (seconds) after the 1st, 2nd, 3rd and 4th incorrect attempts
LOCKOUT_SECONDS = [5, 15, 30, 300]

ID_MAX_DIGITS = 14
ID_MAX_HYPHENS = 3

# Password rules for NEW passwords (create account / reset password)
PASSWORD_MIN = 8
PASSWORD_MAX = 13
PASSWORD_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
PASSWORD_HINT = "8-13 characters: letters, numbers, \"_\" and \"-\" only"

DATE_FORMAT = "%m-%d-%Y"


def check_new_password(pwd):
    """Return an error message if the password breaks the rules, else None."""
    if len(pwd) < PASSWORD_MIN or len(pwd) > PASSWORD_MAX:
        return f"Password must be {PASSWORD_MIN} to {PASSWORD_MAX} characters long."
    if not PASSWORD_PATTERN.match(pwd):
        return "Password may only contain letters, numbers, \"_\" and \"-\"."
    return None


# ==========================================================
# PASSWORD ENTRY WITH EYE ICON (open / closed)
# ==========================================================

class PasswordEntry(tk.Frame):
    """Entry with a placeholder and a drawn eye icon.
    Closed eye = password hidden (dots)
    Open eye = password visible
    Only the icon changes when clicked.

    restrict=True -> max 13 characters, only letters/numbers/_/-,
                      and the first letter is automatically uppercase."""

    def __init__(
        self,
        parent,
        placeholder="Password",
        bg="white",
        fg="#123F87",
        placeholder_fg="#60799B",
        font=("Arial", 12),
        border_color=None,
        border_width=0,
        eye_color="#557AA7",
        ipady=0,
        restrict=False,
    ):
        super().__init__(
            parent,
            bg=bg,
            highlightbackground=border_color or bg,
            highlightcolor=border_color or bg,
            highlightthickness=border_width,
        )

        self.placeholder = placeholder
        self.bg = bg
        self.fg = fg
        self.placeholder_fg = placeholder_fg
        self.eye_color = eye_color
        self.hidden = True
        self.has_placeholder = True
        self.restrict = restrict

        self.eye = tk.Canvas(
            self, width=28, height=28, bg=bg, highlightthickness=0, cursor="hand2"
        )
        self.eye.pack(side="right", padx=(0, 6))
        self.eye.bind("<Button-1>", lambda e: self.toggle())

        entry_options = {}
        if restrict:
            entry_options["validate"] = "key"
            entry_options["validatecommand"] = (self.register(self._validate), "%P")

        self.entry = tk.Entry(
            self,
            font=font,
            bd=0,
            relief="flat",
            bg=bg,
            fg=placeholder_fg,
            highlightthickness=0,
            insertbackground=fg,
            **entry_options,
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(8, 4), ipady=ipady)

        self.entry.bind("<FocusIn>", self._focus_in)
        self.entry.bind("<FocusOut>", self._focus_out)

        if restrict:
            self.entry.bind("<KeyRelease>", self._auto_capitalize)

        self._show_placeholder()
        self._draw_eye()

    # ---------- restriction handling ----------
    def _validate(self, proposed):
        if self.has_placeholder:
            return True
        if len(proposed) > PASSWORD_MAX:
            return False
        return all(ch.isascii() and (ch.isalnum() or ch in "_-") for ch in proposed)

    def _auto_capitalize(self, event=None):
        if self.has_placeholder:
            return
        text = self.entry.get()
        if text and text[0].isalpha() and text[0].islower():
            pos = self.entry.index(tk.INSERT)
            self.entry.delete(0, 1)
            self.entry.insert(0, text[0].upper())
            self.entry.icursor(pos)

    # ---------- placeholder handling ----------
    def _show_placeholder(self):
        self.has_placeholder = True
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=self.placeholder_fg, show="")

    def _focus_in(self, event=None):
        if self.has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.fg)
            self.has_placeholder = False
            self._apply_show()

    def _focus_out(self, event=None):
        if not self.has_placeholder and self.entry.get() == "":
            self._show_placeholder()

    # ---------- eye handling ----------
    def _apply_show(self):
        if self.has_placeholder:
            self.entry.config(show="")
        else:
            self.entry.config(show="•" if self.hidden else "")

    def toggle(self):
        self.hidden = not self.hidden
        self._apply_show()
        self._draw_eye()

    def _draw_eye(self):
        c = self.eye
        col = self.eye_color
        c.delete("all")

        # almond-shaped eye outline
        c.create_polygon(
            2, 14, 8, 8, 14, 6, 20, 8, 26, 14, 20, 20, 14, 22, 8, 20,
            smooth=True, fill="", outline=col, width=2,
        )
        # pupil
        c.create_oval(10, 10, 18, 18, fill=col, outline="")

        if self.hidden:
            # closed eye = slash through the icon
            c.create_line(5, 24, 24, 4, fill=self.bg, width=5)
            c.create_line(5, 24, 24, 4, fill=col, width=2)

    # ---------- public API ----------
    def get(self):
        return "" if self.has_placeholder else self.entry.get()

    def clear(self):
        self._show_placeholder()
        self.hidden = True
        self._draw_eye()


class BorrowiseApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Borrowise")

        # ==================================================
        # WINDOW SETTINGS
        # ==================================================

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        try:
            self.root.state("zoomed")
        except:
            pass

        # ==================================================
        # TEMPORARY LOGIN ACCOUNT
        # ==================================================

        self.registered_accounts = {
            "03-01-2627-001668": {
                "password": "borrowise123",
                "fullname": "Administrator",
                "security_question": SECURITY_QUESTIONS[3],
                "security_answer": "blue",
            }
        }

        self.current_user = {
            "id": "03-01-2627-001668",
            "fullname": "Administrator",
            "security_question": SECURITY_QUESTIONS[3],
        }

        self.failed_attempts = 0
        self.lockout_until = 0
        self.lockout_popup = None

        self.records = []

        # ==================================================
        # COLORS
        # ==================================================

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

        # ==================================================
        # INPUT VALIDATION
        # ==================================================

        self.id_placeholders = {"ID Number", "e.g., 03-01-2627-001668"}
        self.vcmd_id = (self.root.register(self.validate_id_input), "%P")
        self.vcmd_date = (self.root.register(self.validate_date_input), "%P")

        # ==================================================
        # TKINTER STYLES
        # ==================================================

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Borrowise.Treeview",
            background="#F8FCFF",
            fieldbackground="#F8FCFF",
            foreground="#123F87",
            font=("Arial", 12),
            rowheight=42,
            borderwidth=1,
            relief="solid"
        )

        style.configure(
            "Borrowise.Treeview.Heading",
            background="#DDF1FC",
            foreground="#123F87",
            font=("Arial", 12, "bold"),
            padding=12,
            relief="flat"
        )

        style.map(
            "Borrowise.Treeview",
            background=[("selected", "#B9DDF5")],
            foreground=[("selected", "#123F87")]
        )

        style.map(
            "Borrowise.Treeview.Heading",
            background=[("active", "#C8E5FA")]
        )

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

        self.root.option_add("*TCombobox*Listbox.font", ("Arial", 12))

        self.show_login()

    def generate_next_borrower_id(self):
        prefix = "01-01-2627-"
        count = len(self.records) + 1
        return f"{prefix}{count:05d}"

    def validate_id_input(self, proposed):
        if proposed in self.id_placeholders:
            return True

        digits = 0
        hyphens = 0

        for ch in proposed:
            if ch.isdigit() and ch.isascii():
                digits += 1
            elif ch == "-":
                hyphens += 1
            else:
                return False

        return digits <= ID_MAX_DIGITS and hyphens <= ID_MAX_HYPHENS

    def validate_date_input(self, proposed):
        if len(proposed) > 10:
            return False
        return all((ch.isdigit() and ch.isascii()) or ch == "-" for ch in proposed)

    def bind_placeholder(self, entry, placeholder, normal_fg, placeholder_fg):
        def focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=normal_fg)

        def focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg=placeholder_fg)

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)

    def center_popup(self, popup, width, height):
        popup.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - width // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - height // 2
        popup.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")

    def make_question_combo(self, parent, **kwargs):
        combo = ttk.Combobox(
            parent,
            values=SECURITY_QUESTIONS,
            state="readonly",
            style="Borrowise.TCombobox",
            font=("Arial", 12),
            **kwargs
        )
        combo.set(QUESTION_PLACEHOLDER)
        combo.bind("<<ComboboxSelected>>", lambda e: combo.selection_clear())
        return combo

    def show_login(self):
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
        cx = self.center_x
        cy = 150

        self.background.create_polygon(
            cx, cy - 40,
            cx + 45, cy - 15,
            cx, cy + 12,
            cx - 45, cy - 15,
            fill="#F5FAFF",
            outline="#1555A5",
            width=3,
        )
        self.background.create_polygon(
            cx - 45, cy - 15,
            cx, cy + 12,
            cx, cy + 62,
            cx - 45, cy + 35,
            fill="#BFE1FA",
            outline="#1555A5",
            width=3,
        )
        self.background.create_polygon(
            cx, cy + 12,
            cx + 45, cy - 15,
            cx + 45, cy + 35,
            cx, cy + 62,
            fill="#8CC9F1",
            outline="#1555A5",
            width=3,
        )
        self.background.create_text(
            self.center_x,
            240,
            text="Borrowise",
            font=("Arial", 38, "bold"),
            fill="#0E3B82",
        )
        self.background.create_text(
            self.center_x,
            277,
            text="SURPLUS",
            font=("Arial", 15, "bold"),
            fill="#5A78A0",
        )

    def make_login_frame(self, y):
        frame = tk.Frame(
            self.root,
            bg="#FFFFFF",
            highlightbackground=self.border_blue,
            highlightthickness=2,
        )
        frame.place(x=self.center_x, y=y, width=420, height=54, anchor="center")
        return frame

    def create_login_form(self):
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

        self.root.bind("<Return>", lambda event: self.login())

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
        if time.time() < self.lockout_until:
            self.show_lockout_popup()
            return

        id_num = self.id_entry.get().strip()
        password = self.password_field.get()

        if id_num == "ID Number":
            id_num = ""

        account = self.registered_accounts.get(id_num)

        authenticated = bool(
            account
            and account["password"] == password
        )

        if authenticated:
            self.failed_attempts = 0
            self.lockout_until = 0
            self.current_user = {
                "id": id_num,
                "fullname": account.get("fullname", id_num),
                "security_question": account.get("security_question", SECURITY_QUESTIONS[0]),
            }
            self.root.unbind("<Return>")
            self.show_dashboard()
            return

        self.failed_attempts += 1
        seconds = LOCKOUT_SECONDS[min(self.failed_attempts, len(LOCKOUT_SECONDS)) - 1]
        self.lockout_until = time.time() + seconds
        self.password_field.clear()
        self.show_lockout_popup()

    def show_lockout_popup(self):
        if self.lockout_popup is not None:
            try:
                if self.lockout_popup.winfo_exists():
                    self.lockout_popup.lift()
                    return
            except tk.TclError:
                pass

        warning_no = min(self.failed_attempts, len(LOCKOUT_SECONDS))
        total_seconds = LOCKOUT_SECONDS[warning_no - 1]

        popup = tk.Toplevel(self.root)
        self.lockout_popup = popup
        popup.title("Login Warning")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
        self.center_popup(popup, 460, 340)
        popup.grab_set()

        tk.Label(
            popup,
            text="⚠️",
            font=("Segoe UI Emoji", 36),
            fg="#E74C3C",
            bg="white",
        ).pack(pady=(20, 0))

        tk.Label(
            popup,
            text=f"Warning {warning_no} of {len(LOCKOUT_SECONDS)}",
            font=("Arial", 18, "bold"),
            fg="#A93226",
            bg="white",
        ).pack(pady=(5, 0))

        if warning_no >= len(LOCKOUT_SECONDS):
            message = "Too many incorrect attempts.\nYou are locked out for 5 minutes."
        else:
            message = "Incorrect ID Number or password."

        tk.Label(
            popup,
            text=message,
            font=("Arial", 11),
            fg=self.text_blue,
            bg="white",
            justify="center",
        ).pack(pady=(8, 8))

        countdown_label = tk.Label(
            popup,
            text="",
            font=("Arial", 26, "bold"),
            fg=self.dark_blue,
            bg="white",
        )
        countdown_label.pack()

        tk.Label(
            popup,
            text="Please wait before trying again.",
            font=("Arial", 10),
            fg=self.text_gray,
            bg="white",
        ).pack(pady=(0, 10))

        ok_button = tk.Button(
            popup,
            text="Please wait...",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#9CB6D1",
            relief="flat",
            bd=0,
            padx=40,
            pady=8,
            state="disabled",
            command=popup.destroy,
        )
        ok_button.pack()

        def format_time(secs):
            return f"{secs // 60:02d}:{secs % 60:02d}"

        def tick():
            remaining = max(0, math.ceil(self.lockout_until - time.time()))
            countdown_label.config(text=format_time(remaining))

            if remaining > 0:
                popup.after(250, tick)
            else:
                ok_button.config(
                    text="OK", state="normal", bg=self.blue, cursor="hand2",
                    activebackground="#087DDC", activeforeground="white",
                )
                popup.protocol("WM_DELETE_WINDOW", popup.destroy)

        tick()

    def popup_label(self, popup, text):
        tk.Label(
            popup,
            text=text,
            font=("Arial", 10, "bold"),
            fg=self.text_blue,
            bg="white",
        ).pack(anchor="w", padx=35)

    def popup_hint(self, popup, text, pady=(0, 8)):
        tk.Label(
            popup,
            text=text,
            font=("Arial", 10, "bold"),
            fg=self.text_gray,
            bg="white",
        ).pack(anchor="w", padx=35, pady=pady)

    def open_forgot_password_window(self):
        popup = tk.Toplevel(self.root)
        popup.title("Forgot Password")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        self.center_popup(popup, 420, 480)
        popup.grab_set()

        tk.Label(
            popup,
            text="Reset Password",
            font=("Arial", 18, "bold"),
            fg=self.dark_blue,
            bg="white",
        ).pack(pady=(25, 15))

        self.popup_label(popup, "ID Number:")
        id_placeholder = "e.g., 03-01-2627-001668"
        f_id = tk.Entry(
            popup,
            font=("Arial", 12),
            fg=self.text_gray,
            bg="#F5FAFF",
            relief="solid",
            bd=1,
            validate="key",
            validatecommand=self.vcmd_id,
        )
        f_id.pack(fill="x", padx=35, pady=(5, 12), ipady=5)
        f_id.insert(0, id_placeholder)
        self.bind_placeholder(f_id, id_placeholder, "#123F87", self.text_gray)

        self.popup_label(popup, "Enter New Password:")
        f_pass = PasswordEntry(
            popup,
            placeholder="New password",
            bg="#F5FAFF",
            font=("Arial", 12),
            border_color="#7F9DB9",
            border_width=1,
            ipady=5,
            restrict=True,
        )
        f_pass.pack(fill="x", padx=35, pady=(5, 3))
        self.popup_hint(popup, PASSWORD_HINT, pady=(0, 14))

        def reset_action():
            acc_id = f_id.get().strip()
            new_pass = f_pass.get().strip()

            if acc_id == id_placeholder:
                acc_id = ""

            if not acc_id or not new_pass:
                messagebox.showwarning(
                    "Warning", "Please fill in all fields.", parent=popup
                )
                return

            error = check_new_password(new_pass)
            if error:
                messagebox.showerror("Error", error, parent=popup)
                return

            account = self.registered_accounts.get(acc_id)

            if account:
                account["password"] = new_pass
                messagebox.showinfo(
                    "Success",
                    "Password has been reset successfully!",
                    parent=popup,
                )
                popup.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "ID Number is incorrect or does not exist.",
                    parent=popup,
                )

        tk.Button(
            popup,
            text="RESET PASSWORD",
            font=("Arial", 11, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#087DDC",
            relief="flat",
            cursor="hand2",
            command=reset_action,
        ).pack(fill="x", padx=35, ipady=8)

    def open_create_account_window(self):
        popup = tk.Toplevel(self.root)
        popup.title("Create New Account")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        self.center_popup(popup, 440, 700)
        popup.grab_set()

        tk.Label(
            popup,
            text="Create New Account",
            font=("Arial", 18, "bold"),
            fg=self.dark_blue,
            bg="white",
        ).pack(pady=(20, 10))

        self.popup_label(popup, "ID Number:")

        id_placeholder = "e.g., 03-01-2627-001668"
        id_entry = tk.Entry(
            popup,
            font=("Arial", 12),
            fg="#60799B",
            bg="#F5FAFF",
            relief="solid",
            bd=1,
            validate="key",
            validatecommand=self.vcmd_id,
        )
        id_entry.pack(fill="x", padx=35, pady=(3, 10), ipady=4)
        id_entry.insert(0, id_placeholder)
        self.bind_placeholder(id_entry, id_placeholder, "#123F87", "#60799B")

        self.popup_label(popup, "Full Name:")

        name_entry = tk.Entry(
            popup, font=("Arial", 12), bg="#F5FAFF", relief="solid", bd=1
        )
        name_entry.pack(fill="x", padx=35, pady=(3, 10), ipady=4)

        self.popup_label(popup, "Security Question:")

        question_combo = self.make_question_combo(popup)
        question_combo.pack(fill="x", padx=35, pady=(3, 10), ipady=3)

        self.popup_label(popup, "Security Answer:")

        answer_entry = tk.Entry(
            popup, font=("Arial", 12), bg="#F5FAFF", relief="solid", bd=1
        )
        answer_entry.pack(fill="x", padx=35, pady=(3, 10), ipady=4)

        self.popup_label(popup, "Password:")

        p_entry = PasswordEntry(
            popup,
            placeholder="Password",
            bg="#F5FAFF",
            font=("Arial", 12),
            border_color="#7F9DB9",
            border_width=1,
            ipady=4,
            restrict=True,
        )
        p_entry.pack(fill="x", padx=35, pady=(3, 10))

        self.popup_label(popup, "Confirm Password:")

        cp_entry = PasswordEntry(
            popup,
            placeholder="Confirm password",
            bg="#F5FAFF",
            font=("Arial", 12),
            border_color="#7F9DB9",
            border_width=1,
            ipady=4,
            restrict=True,
        )
        cp_entry.pack(fill="x", padx=35, pady=(3, 15))

        def save_account():
            new_id = id_entry.get().strip()
            fullname = name_entry.get().strip()
            question = question_combo.get()
            answer = answer_entry.get().strip()
            pwd = p_entry.get()
            cpwd = cp_entry.get()

            if (
                not new_id
                or new_id == id_placeholder
                or not fullname
                or question == QUESTION_PLACEHOLDER
                or not answer
                or not pwd
                or not cpwd
            ):
                messagebox.showwarning(
                    "Warning", "Please fill in all fields.", parent=popup
                )
                return

            error = check_new_password(pwd)
            if error:
                messagebox.showerror("Error", error, parent=popup)
                return

            if pwd != cpwd:
                messagebox.showerror(
                    "Error", "Passwords do not match!", parent=popup
                )
                return

            if new_id in self.registered_accounts:
                messagebox.showerror(
                    "Error",
                    "An account with this ID Number already exists!",
                    parent=popup,
                )
                return

            self.registered_accounts[new_id] = {
                "password": pwd,
                "fullname": fullname,
                "security_question": question,
                "security_answer": answer,
            }

            messagebox.showinfo(
                "Success",
                "Account created successfully! You can now log in.",
                parent=popup,
            )
            popup.destroy()

        tk.Button(
            popup,
            text="Create Account",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#087DDC",
            relief="flat",
            cursor="hand2",
            command=save_account,
        ).pack(fill="x", padx=35, ipady=8)

        link_frame = tk.Frame(popup, bg="white")
        link_frame.pack(pady=10)

        tk.Label(
            link_frame,
            text="Already have an account?",
            font=("Arial", 9),
            fg="gray",
            bg="white",
        ).pack(side="left")

        login_link = tk.Label(
            link_frame,
            text=" Log in",
            font=("Arial", 9, "bold"),
            fg=self.blue,
            bg="white",
            cursor="hand2",
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: (popup.destroy()))

    def create_card_icon(self, parent, x, y):
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        color = "#557AA7"

        canvas.create_rectangle(3, 8, 37, 32, outline=color, width=3)
        canvas.create_oval(8, 13, 17, 22, fill=color, outline="")
        canvas.create_arc(6, 22, 20, 36, start=0, extent=180, fill=color, outline="")
        canvas.create_line(23, 15, 33, 15, fill=color, width=2)
        canvas.create_line(23, 21, 33, 21, fill=color, width=2)
        canvas.create_line(23, 27, 30, 27, fill=color, width=2)

    def create_question_icon(self, parent, x, y):
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        color = "#557AA7"

        canvas.create_oval(5, 5, 35, 35, outline=color, width=3)
        canvas.create_text(20, 20, text="?", font=("Arial", 15, "bold"), fill=color)

    def create_key_icon(self, parent, x, y):
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        color = "#557AA7"

        canvas.create_oval(5, 10, 21, 26, outline=color, width=3)
        canvas.create_line(21, 18, 36, 18, fill=color, width=3)
        canvas.create_line(30, 18, 30, 25, fill=color, width=3)
        canvas.create_line(35, 18, 35, 24, fill=color, width=3)

    def create_lock_icon(self, parent, x, y):
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        lock_color = "#557AA7"
        canvas.create_arc(
            10, 4, 30, 24,
            start=0,
            extent=180,
            style="arc",
            outline=lock_color,
            width=4,
        )
        canvas.create_line(10, 14, 10, 19, fill=lock_color, width=4)
        canvas.create_line(30, 14, 30, 19, fill=lock_color, width=4)
        canvas.create_rectangle(8, 17, 32, 36, fill=lock_color, outline="")
        canvas.create_oval(18, 21, 22, 25, fill="white", outline="")
        canvas.create_rectangle(19, 24, 21, 29, fill="white", outline="")

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self.root, bg="#F2FAFF")
        self.main_frame.pack(fill="both", expand=True)

        self.create_sidebar()

        self.content_frame = tk.Frame(self.main_frame, bg="#F2FAFF")
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.dashboard_home()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, bg="#063B73", width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_frame = tk.Frame(self.sidebar, bg="#063B73")
        logo_frame.pack(fill="x", padx=25, pady=(35, 20))

        tk.Label(
            logo_frame,
            text="📦",
            font=("Segoe UI Emoji", 43),
            fg="#CBEAFF",
            bg="#063B73",
        ).pack(side="left")

        logo_text = tk.Frame(logo_frame, bg="#063B73")
        logo_text.pack(side="left", padx=10)

        tk.Label(
            logo_text,
            text="Borrowise",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#063B73",
        ).pack(anchor="w")

        tk.Label(
            logo_text,
            text="SURPLUS",
            font=("Arial", 13, "bold"),
            fg="#B9DDF5",
            bg="#063B73",
        ).pack(anchor="center", pady=(2, 0))

        nav_container = tk.Frame(self.sidebar, bg="#063B73")
        nav_container.pack(fill="both", expand=True)

        self.create_sidebar_button(nav_container, " 🏠", " Home", self.dashboard_home)
        self.create_sidebar_button(nav_container, " ➕", "Borrow Item", self.show_borrow)
        self.create_sidebar_button(nav_container, " 📦", "Return Item", self.show_return)
        self.create_sidebar_button(nav_container, " 📋", " Records", self.show_records)
        self.create_sidebar_button(nav_container, " 🔍", " Search", self.show_search)
        self.create_sidebar_button(nav_container, " ↪", " Logout", self.logout)

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

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def page_title(self, title, subtitle, action=None):
        header = tk.Frame(self.content_frame, bg="#F2FAFF")
        header.pack(fill="x", padx=45, pady=(40, 25))

        left = tk.Frame(header, bg="#F2FAFF")
        left.pack(side="left")

        tk.Label(
            left,
            text=title,
            font=("Arial", 32, "bold"),
            fg="#123A8C",
            bg="#F2FAFF",
        ).pack(anchor="w", pady=(0, 3))

        tk.Label(
            left,
            text=subtitle,
            font=("Arial", 15),
            fg="#6689A8",
            bg="#F2FAFF",
        ).pack(anchor="w")

        if action is not None:
            widget = action(header)
            widget.pack(side="right", anchor="n", pady=(8, 0))

    def create_container(self, parent):
        container = tk.Frame(
            parent,
            bg="#F8FCFF",
            highlightbackground="#B9DDF5",
            highlightcolor="#B9DDF5",
            highlightthickness=2,
        )
        return container

    def show_profile(self):
        self.clear_content()

        self.page_title("My Profile", "View and manage your account information.")

        profile_card = tk.Frame(
            self.content_frame,
            bg="#F8FCFF",
            highlightbackground="#DDF1FC",
            highlightthickness=2
        )
        profile_card.pack(fill="x", padx=45, pady=(0, 25), ipady=15)

        left_profile = tk.Frame(profile_card, bg="#F8FCFF")
        left_profile.pack(side="left", padx=40, pady=20)

        avatar_canvas = tk.Canvas(left_profile, width=110, height=110, bg="#F8FCFF", highlightthickness=0)
        avatar_canvas.pack(side="left")

        avatar_canvas.create_oval(5, 5, 105, 105, fill="#D8EBFA", outline="")
        avatar_canvas.create_oval(40, 25, 70, 55, fill="#0E3B82", outline="")
        avatar_canvas.create_arc(20, 58, 90, 115, start=0, extent=180, fill="#0E3B82", outline="")

        user_info_frame = tk.Frame(left_profile, bg="#F8FCFF")
        user_info_frame.pack(side="left", padx=20)

        name_str = self.current_user.get("fullname", "USER").upper()
        id_str = self.current_user.get("id", "ID Number")

        tk.Label(
            user_info_frame,
            text=name_str,
            font=("Arial", 28, "bold"),
            fg="#0E3B82",
            bg="#F8FCFF"
        ).pack(anchor="w")

        tk.Label(
            user_info_frame,
            text=f"ID Number: {id_str}",
            font=("Arial", 14),
            fg="#6689A8",
            bg="#F8FCFF"
        ).pack(anchor="w", pady=(2, 0))

        divider = tk.Frame(profile_card, bg="#B9DDF5", width=2)
        divider.pack(side="left", fill="y", pady=20)

        right_details = tk.Frame(profile_card, bg="#F8FCFF")
        right_details.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        header_frame = tk.Frame(right_details, bg="#F8FCFF")
        header_frame.pack(anchor="w", pady=(0, 15))

        tk.Label(
            header_frame,
            text="🪪",
            font=("Segoe UI Emoji", 14),
            bg="#F8FCFF"
        ).pack(side="left", padx=(0, 5))

        tk.Label(
            header_frame,
            text="ACCOUNT DETAILS",
            font=("Arial", 14, "bold"),
            fg="#0E3B82",
            bg="#F8FCFF"
        ).pack(side="left")

        fields = [
            ("ID Number :", self.current_user.get("id", "")),
            ("Full Name :", self.current_user.get("fullname", "")),
        ]

        for label_text, val in fields:
            row_f = tk.Frame(right_details, bg="#F8FCFF")
            row_f.pack(fill="x", pady=4)

            tk.Label(
                row_f,
                text=label_text,
                font=("Arial", 12, "bold"),
                fg="#123F87",
                bg="#F8FCFF",
                width=18,
                anchor="w"
            ).pack(side="left")

            entry_box = tk.Entry(
                row_f,
                font=("Arial", 11),
                fg="#123F87",
                bg="#F2F8FD",
                relief="solid",
                bd=1
            )
            entry_box.pack(side="left", fill="x", expand=True, ipady=4, padx=5)
            entry_box.insert(0, val)
            entry_box.config(state="readonly")

        summary_card = tk.Frame(
            self.content_frame,
            bg="#F8FCFF",
            highlightbackground="#DDF1FC",
            highlightthickness=2
        )
        summary_card.pack(fill="both", expand=True, padx=45, pady=(0, 25), ipady=15)

        sum_header = tk.Frame(summary_card, bg="#F8FCFF")
        sum_header.pack(fill="x", padx=25, pady=(15, 5))

        tk.Label(
            sum_header,
            text="📊 Borrowise Summary",
            font=("Arial", 16, "bold"),
            fg="#0E3B82",
            bg="#F8FCFF"
        ).pack(anchor="w")

        tk.Label(
            sum_header,
            text="Quick overview of your borrowing activity.",
            font=("Arial", 11),
            fg="#6689A8",
            bg="#F8FCFF"
        ).pack(anchor="w")

        sum_cards_frame = tk.Frame(summary_card, bg="#F8FCFF")
        sum_cards_frame.pack(fill="x", padx=25, pady=15)

        for col in range(3):
            sum_cards_frame.grid_columnconfigure(col, weight=1, uniform="sum_cards")

        borrowed_count = sum(1 for r in self.records if r.get("status") == "Borrowed")
        returned_count = sum(1 for r in self.records if r.get("status") == "Returned")
        overdue_count = sum(1 for r in self.records if r.get("status") in ["Lost", "Damaged"])

        c1 = tk.Frame(sum_cards_frame, bg="#EBF5FC", highlightbackground="#3A9AD9", highlightthickness=1)
        c1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(c1, text="📦", font=("Segoe UI Emoji", 20), bg="#EBF5FC").pack(side="left", padx=15, pady=15)
        c1_text = tk.Frame(c1, bg="#EBF5FC")
        c1_text.pack(side="left", pady=10)
        tk.Label(c1_text, text="Currently Borrowed", font=("Arial", 11, "bold"), fg="#123F87", bg="#EBF5FC").pack(anchor="w")
        tk.Label(c1_text, text=str(borrowed_count), font=("Arial", 22, "bold"), fg="#123F87", bg="#EBF5FC").pack(anchor="w")
        tk.Label(c1_text, text="Items", font=("Arial", 9), fg="#6689A8", bg="#EBF5FC").pack(anchor="w")

        c2 = tk.Frame(sum_cards_frame, bg="#EBF8F2", highlightbackground="#27B96F", highlightthickness=1)
        c2.grid(row=0, column=1, sticky="nsew", padx=5)

        tk.Label(c2, text="🔄", font=("Segoe UI Emoji", 20), bg="#EBF8F2").pack(side="left", padx=15, pady=15)
        c2_text = tk.Frame(c2, bg="#EBF8F2")
        c2_text.pack(side="left", pady=10)
        tk.Label(c2_text, text="Return Items", font=("Arial", 11, "bold"), fg="#197D49", bg="#EBF8F2").pack(anchor="w")
        tk.Label(c2_text, text=str(returned_count), font=("Arial", 22, "bold"), fg="#197D49", bg="#EBF8F2").pack(anchor="w")
        tk.Label(c2_text, text="Items", font=("Arial", 9), fg="#5EA680", bg="#EBF8F2").pack(anchor="w")

        c3 = tk.Frame(sum_cards_frame, bg="#FDEAEA", highlightbackground="#E74C3C", highlightthickness=1)
        c3.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        tk.Label(c3, text="⚠️", font=("Segoe UI Emoji", 20), bg="#FDEAEA").pack(side="left", padx=15, pady=15)
        c3_text = tk.Frame(c3, bg="#FDEAEA")
        c3_text.pack(side="left", pady=10)
        tk.Label(c3_text, text="Overdue Items", font=("Arial", 11, "bold"), fg="#A93226", bg="#FDEAEA").pack(anchor="w")
        tk.Label(c3_text, text=str(overdue_count), font=("Arial", 22, "bold"), fg="#A93226", bg="#FDEAEA").pack(anchor="w")
        tk.Label(c3_text, text="Item" if overdue_count == 1 else "Items", font=("Arial", 9), fg="#C07870", bg="#FDEAEA").pack(anchor="w")

    def dashboard_home(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Welcome to Borrowise!",
            font=("Arial", 36, "bold"),
            fg="#123A8C",
            bg="#F2FAFF",
        ).pack(anchor="w", padx=45, pady=(40, 3))

        tk.Label(
            self.content_frame,
            text="Easily manage and monitor your borrowed items.",
            font=("Arial", 16),
            fg="#6689A8",
            bg="#F2FAFF",
        ).pack(anchor="w", padx=45, pady=(0, 28))

        cards_frame = tk.Frame(
            self.content_frame,
            bg="#F2FAFF"
        )
        cards_frame.pack(
            fill="x",
            padx=45
        )

        card_gap = 12

        for column in range(4):
            cards_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="dashboard_cards"
            )

        borrow_card = self.create_dashboard_card(
            cards_frame,
            "➕",
            "Borrow\nItem",
            "#168CF5",
            self.show_borrow
        )
        borrow_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, card_gap // 2)
        )

        return_card = self.create_dashboard_card(
            cards_frame,
            "📦",
            "Return\nItem",
            "#27B96F",
            self.show_return
        )
        return_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=card_gap // 2
        )

        records_card = self.create_dashboard_card(
            cards_frame,
            "📋",
            "View\nRecords",
            "#7655E8",
            self.show_records
        )
        records_card.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=card_gap // 2
        )

        search_card = self.create_dashboard_card(
            cards_frame,
            "🔍",
            "Search\nRecords",
            "#F5A623",
            self.show_search
        )
        search_card.grid(
            row=0,
            column=3,
            sticky="nsew",
            padx=(card_gap // 2, 0)
        )

        quote_container = tk.Frame(
            self.content_frame,
            bg="#E8F6FD",
            highlightbackground="#B9DDF5",
            highlightthickness=2,
        )
        quote_container.pack(fill="x", padx=45, pady=40, ipady=22)

        tk.Label(
            quote_container, text="📦", font=("Segoe UI Emoji", 38), bg="#E8F6FD"
        ).pack(side="left", padx=(35, 20))

        quote_text = tk.Frame(quote_container, bg="#E8F6FD")
        quote_text.pack(side="left")

        tk.Label(
            quote_text,
            text="“Borrowise smart. Keep track.”",
            font=("Arial", 19, "bold"),
            fg="#123A8C",
            bg="#E8F6FD",
        ).pack(anchor="w")

        tk.Label(
            quote_text,
            text="— Borrowise",
            font=("Arial", 13),
            fg="#6689A8",
            bg="#E8F6FD",
        ).pack(anchor="w", pady=(4, 0))

    def create_dashboard_card(self, parent, icon, text, color, command):
        card = tk.Frame(parent, bg=color, height=205, cursor="hand2")
        card.pack_propagate(False)

        icon_label = tk.Label(
            card, text=icon, font=("Segoe UI Emoji", 40), fg="white", bg=color
        )
        icon_label.pack(pady=28)

        text_label = tk.Label(
            card,
            text=text,
            font=("Arial", 18, "bold"),
            fg="white",
            bg=color,
            justify="center",
        )
        text_label.pack()

        card.bind("<Button-1>", lambda event: command())
        icon_label.bind("<Button-1>", lambda event: command())
        text_label.bind("<Button-1>", lambda event: command())

        return card

    def show_borrow(self):
        self.clear_content()

        self.page_title(
            "Borrow Item", "Enter the details of the item to be borrowed."
        )

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        form = tk.Frame(container, bg="#F8FCFF")
        form.pack(fill="x", padx=25, pady=25)

        next_id = self.generate_next_borrower_id()
        self.borrower_id_entry = self.create_fixed_status_row(
            form, "ID Number:", next_id
        )

        self.borrower_entry = self.create_entry_row(
            form, "Borrower Name:", "Enter name"
        )

        self.item_combo = self.create_combo_row(
            form,
            "Item Selection:",
            [
                "Select item",
                "Laptop",
                "Projector",
                "Keyboard",
                "Mouse",
                "Calculator",
                "Monitor",
                "Extension Cord",
                "Speaker",
            ],
        )

        self.quantity_spin = self.create_spinbox_row(form, "Quantity:")

        today = datetime.now().strftime(DATE_FORMAT)
        self.borrow_date_entry = self.create_fixed_status_row(
            form, "Borrowing Date:", today
        )

        self.expected_return_entry = self.create_date_row(
            form, "Expected Return Date:", today
        )

        self.status_entry = self.create_fixed_status_row(form, "Status:", "Borrowed")

        button_frame = tk.Frame(form, bg="#F8FCFF")
        button_frame.pack(pady=(18, 5))

        tk.Button(
            button_frame,
            text="Save / Borrow",
            font=("Arial", 15, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#087DDC",
            relief="flat",
            bd=0,
            padx=45,
            pady=12,
            cursor="hand2",
            command=self.borrow_item,
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 15, "bold"),
            fg=self.text_blue,
            bg="#DCEFFC",
            activebackground="#CBE9FA",
            relief="flat",
            bd=0,
            padx=45,
            pady=12,
            cursor="hand2",
            command=self.clear_borrow_form,
        ).pack(side="left", padx=8)

    def create_fixed_status_row(self, parent, label_text, status_value):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF",
            width=22,
            anchor="w",
        ).pack(side="left")

        entry_container = tk.Frame(
            row,
            bg="white",
            highlightbackground=self.line_color,
            highlightcolor=self.line_color,
            highlightthickness=2,
        )
        entry_container.pack(side="left", fill="x", expand=True)

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
        entry.config(state="disabled")

        return entry

    def create_date_row(self, parent, label_text, default_value, allow_past=False):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF",
            width=22,
            anchor="w",
        ).pack(side="left")

        entry_container = tk.Frame(
            row,
            bg="white",
            highlightbackground=self.line_color,
            highlightcolor=self.line_color,
            highlightthickness=2,
        )
        entry_container.pack(side="left", fill="x", expand=True)

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

    def open_calendar(self, target_entry, allow_past=False):
        try:
            current = datetime.strptime(target_entry.get().strip(), DATE_FORMAT)
        except ValueError:
            current = datetime.now()

        today = datetime.now().date()
        selected = current.date()
        state = {"year": current.year, "month": current.month}

        popup = tk.Toplevel(self.root)
        popup.title("Select Date")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)

        width, height = 340, 370
        x = target_entry.winfo_rootx()
        y = target_entry.winfo_rooty() + target_entry.winfo_height() + 10
        popup.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")
        popup.grab_set()
        popup.bind("<Escape>", lambda e: popup.destroy())

        header = tk.Frame(popup, bg="white")
        header.pack(fill="x", padx=15, pady=(15, 8))

        title_label = tk.Label(
            header, text="", font=("Arial", 14, "bold"), fg=self.dark_blue, bg="white"
        )

        def change_month(delta):
            month = state["month"] + delta
            year = state["year"]
            if month < 1:
                month, year = 12, year - 1
            elif month > 12:
                month, year = 1, year + 1
            state["month"], state["year"] = month, year
            draw_days()

        tk.Button(
            header, text="◀", font=("Arial", 12, "bold"), fg=self.blue, bg="white",
            activebackground="#E8F4FF", relief="flat", bd=0, cursor="hand2",
            command=lambda: change_month(-1),
        ).pack(side="left")
        title_label.pack(side="left", expand=True)
        tk.Button(
            header, text="▶", font=("Arial", 12, "bold"), fg=self.blue, bg="white",
            activebackground="#E8F4FF", relief="flat", bd=0, cursor="hand2",
            command=lambda: change_month(1),
        ).pack(side="right")

        grid = tk.Frame(popup, bg="white")
        grid.pack(padx=15)

        day_names = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        for col, name in enumerate(day_names):
            tk.Label(
                grid, text=name, font=("Arial", 10, "bold"), fg=self.text_gray,
                bg="white", width=4, height=2,
            ).grid(row=0, column=col)

        days_frame = tk.Frame(popup, bg="white")
        days_frame.pack(padx=15)

        def pick(year, month, day):
            target_entry.delete(0, tk.END)
            target_entry.insert(0, datetime(year, month, day).strftime(DATE_FORMAT))
            popup.destroy()

        def draw_days():
            for widget in days_frame.winfo_children():
                widget.destroy()

            year, month = state["year"], state["month"]
            title_label.config(text=f"{calendar.month_name[month]} {year}")

            weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)

            for row, week in enumerate(weeks):
                for col, day in enumerate(week):
                    if day == 0:
                        tk.Label(days_frame, text="", bg="white", width=4, height=2).grid(
                            row=row, column=col
                        )
                        continue

                    this_date = datetime(year, month, day).date()
                    is_past = this_date < today and not allow_past
                    is_selected = this_date == selected

                    if is_past:
                        fg, bg = "#B7C6D6", "white"
                    elif is_selected:
                        fg, bg = "white", self.blue
                    elif this_date == today:
                        fg, bg = self.dark_blue, "#DDF1FC"
                    else:
                        fg, bg = self.dark_blue, "white"

                    tk.Button(
                        days_frame,
                        text=str(day),
                        font=("Arial", 10, "bold" if is_selected else "normal"),
                        fg=fg,
                        bg=bg,
                        activebackground="#B9DDF5",
                        activeforeground=self.dark_blue,
                        relief="flat",
                        bd=0,
                        width=4,
                        height=2,
                        state="disabled" if is_past else "normal",
                        cursor="arrow" if is_past else "hand2",
                        command=lambda y=year, m=month, d=day: pick(y, m, d),
                    ).grid(row=row, column=col, padx=1, pady=1)

        footer = tk.Frame(popup, bg="white")
        footer.pack(side="bottom", fill="x", padx=15, pady=12)

        def go_today():
            pick(today.year, today.month, today.day)

        tk.Button(
            footer, text="Today", font=("Arial", 10, "bold"), fg=self.blue, bg="#E8F4FF",
            activebackground="#CBE9FA", relief="flat", bd=0, padx=16, pady=5,
            cursor="hand2", command=go_today,
        ).pack(side="left")

        tk.Button(
            footer, text="Close", font=("Arial", 10, "bold"), fg=self.text_blue, bg="#F0F4F8",
            activebackground="#DCE5EE", relief="flat", bd=0, padx=16, pady=5,
            cursor="hand2", command=popup.destroy,
        ).pack(side="right")

        draw_days()

    def create_entry_row(self, parent, label_text, placeholder):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF",
            width=22,
            anchor="w",
        ).pack(side="left")

        entry_container = tk.Frame(
            row,
            bg="white",
            highlightbackground=self.line_color,
            highlightcolor=self.line_color,
            highlightthickness=2,
        )
        entry_container.pack(side="left", fill="x", expand=True)

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
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.text_blue)

    def create_combo_row(self, parent, label_text, values):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF",
            width=22,
            anchor="w",
        ).pack(side="left")

        combo_container = tk.Frame(
            row,
            bg="white",
            highlightbackground=self.line_color,
            highlightcolor=self.line_color,
            highlightthickness=2,
        )
        combo_container.pack(side="left", fill="x", expand=True)

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
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF",
            width=22,
            anchor="w",
        ).pack(side="left")

        spin_container = tk.Frame(
            row,
            bg="white",
            highlightbackground=self.line_color,
            highlightthickness=2,
        )
        spin_container.pack(side="left", fill="x", expand=True)

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

    def borrow_item(self):
        borrower_id = self.borrower_id_entry.get().strip()
        name = self.borrower_entry.get().strip()
        item = self.item_combo.get()
        quantity = self.quantity_spin.get().strip()
        borrow_date = self.borrow_date_entry.get().strip()
        return_date = self.expected_return_entry.get().strip()
        status = "Borrowed"

        if borrower_id == "" or borrower_id == "Enter ID number":
            messagebox.showwarning("Borrowise", "Please enter the ID number.")
            return

        if name == "" or name == "Enter name":
            messagebox.showwarning("Borrowise", "Please enter the borrower name.")
            return

        if item == "Select item":
            messagebox.showwarning("Borrowise", "Please select an item.")
            return

        try:
            expected = datetime.strptime(return_date, DATE_FORMAT).date()
        except ValueError:
            messagebox.showwarning(
                "Borrowise",
                "Please enter a valid Expected Return Date (MM-DD-YYYY),\n"
                "or pick one using the calendar button.",
            )
            return

        try:
            borrowed_on = datetime.strptime(borrow_date, DATE_FORMAT).date()
        except ValueError:
            borrowed_on = datetime.now().date()

        if expected < borrowed_on:
            messagebox.showwarning(
                "Borrowise",
                "The Expected Return Date cannot be earlier than the Borrowing Date.",
            )
            return

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
        self.show_success_popup()

    def clear_borrow_form(self):
        self.borrower_id_entry.config(state="normal")
        self.borrower_id_entry.delete(0, tk.END)
        self.borrower_id_entry.insert(0, self.generate_next_borrower_id())
        self.borrower_id_entry.config(state="disabled")

        self.borrower_entry.delete(0, tk.END)
        self.borrower_entry.insert(0, "Enter name")
        self.borrower_entry.config(fg="#47789E")

        self.item_combo.current(0)

        self.quantity_spin.delete(0, tk.END)
        self.quantity_spin.insert(0, "1")

        today = datetime.now().strftime(DATE_FORMAT)
        self.borrow_date_entry.config(state="normal")
        self.borrow_date_entry.delete(0, tk.END)
        self.borrow_date_entry.insert(0, today)
        self.borrow_date_entry.config(state="disabled")

        self.expected_return_entry.delete(0, tk.END)
        self.expected_return_entry.insert(0, today)

    def show_success_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Borrowise")
        popup.geometry("520x300")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        popup.grab_set()
        popup.update_idletasks()

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
            text_frame,
            text="Success!",
            font=("Arial", 20, "bold"),
            fg=self.dark_blue,
            bg="white",
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text="Item has been borrowed successfully.",
            font=("Arial", 10),
            fg=self.text_blue,
            bg="white",
        ).pack(anchor="w", pady=(3, 20))

        def on_popup_close():
            popup.destroy()
            self.clear_borrow_form()

        tk.Button(
            text_frame,
            text="OK",
            font=("Arial", 10, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#087DDC",
            relief="flat",
            bd=0,
            padx=65,
            pady=10,
            command=on_popup_close,
            cursor="hand2",
        ).pack(anchor="w")

    # ======================================================
    # RETURN ITEM
    # ======================================================

    def show_return(self):

        self.clear_content()

        self.page_title(
            "📦 Return Item", "Enter the details of the borrowed item."
        )

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        form = tk.Frame(container, bg="#F8FCFF")
        form.pack(fill="x", padx=25, pady=25)

        self.return_id_entry = self.create_entry_row(
            form, "ID Number:", "Enter ID number"
        )

        self.return_name_entry = self.create_entry_row(
            form, "Borrower Name:", "Enter name"
        )

        self.return_item_entry = self.create_entry_row(form, "Item:", "Enter item")

        # Return Date: Kusang lumalabas ang kasalukuyang petsa ngayon at naka-lock/automatic
        today = datetime.now().strftime(DATE_FORMAT)
        self.return_date_entry = self.create_fixed_status_row(
            form, "Return Date:", today
        )

        return_btn_frame = tk.Frame(form, bg="#F8FCFF")
        return_btn_frame.pack(pady=20)

        tk.Button(
            return_btn_frame,
            text="📦 Mark as Returned",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.green,
            activebackground="#1FA762",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.process_item_status("Returned")
        ).pack(side="left", padx=5)

        tk.Button(
            return_btn_frame,
            text="⚠️ Mark as Lost",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.orange,
            activebackground="#D98E1B",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.process_item_status("Lost")
        ).pack(side="left", padx=5)

        tk.Button(
            return_btn_frame,
            text="❌ Mark as Damaged",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#E74C3C",
            activebackground="#C0392B",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.process_item_status("Damaged")
        ).pack(side="left", padx=5)

        info_frame = tk.Frame(form, bg="#E8F6FD")
        info_frame.pack(fill="x", pady=(5, 5), padx=5)

        tk.Label(
            info_frame,
            text="ⓘ",
            font=("Arial", 20, "bold"),
            fg=self.blue,
            bg="#E8F6FD",
        ).pack(side="left", padx=(15, 10), pady=12)

        tk.Label(
            info_frame,
            text='Return Reminder\nPlease return the borrowed item within 3 weeks. Make sure to update its status on or before the expected return date.',
            font=("Arial", 9),
            fg=self.text_blue,
            bg="#E8F6FD",
            justify="left",
        ).pack(side="left", pady=12)

    def process_item_status(self, new_status):
        borrower_id = self.return_id_entry.get().strip()
        name = self.return_name_entry.get().strip()
        item = self.return_item_entry.get().strip()

        # Kinukuha ang kasalukuyang petsa nang awtomatisado
        return_date = datetime.now().strftime(DATE_FORMAT)

        if borrower_id == "" or borrower_id == "Enter ID number":
            messagebox.showwarning("Borrowise", "Please enter the ID number.")
            return

        if name == "" or name == "Enter name":
            messagebox.showwarning("Borrowise", "Please enter the borrower name.")
            return

        if item == "" or item == "Enter item":
            messagebox.showwarning("Borrowise", "Please enter the item.")
            return

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
                "Borrowise", f"Item status has been successfully updated to '{new_status}'."
            )
            self.show_records()
        else:
            messagebox.showwarning(
                "Borrowise", "No matching active borrowed item was found."
            )

    def create_bordered_table(self, parent, table_name):
        table_container = tk.Frame(
            parent,
            bg="#F8FCFF"
        )
        table_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        canvas = tk.Canvas(
            table_container,
            bg="#F8FCFF",
            highlightthickness=0
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=vertical_scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        table_frame = tk.Frame(
            canvas,
            bg="#C8DDF2"
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=table_frame,
            anchor="nw"
        )

        def center_table(event=None):
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

        setattr(self, f"{table_name}_table_canvas", canvas)
        setattr(self, f"{table_name}_table_frame", table_frame)
        setattr(self, f"{table_name}_table_window", canvas_window)

        return table_frame

    TABLE_COLUMNS = (
        "ID Number",
        "Name",
        "Item",
        "Quantity",
        "Borrow Date",
        "Return Date",
        "Status"
    )

    TABLE_KEYS = (
        "borrower_id",
        "name",
        "item",
        "quantity",
        "borrow_date",
        "return_date",
        "status"
    )

    def populate_bordered_table(self, table_frame, records):
        columns = self.TABLE_COLUMNS

        column_widths = {
            "ID Number": 18,
            "Name": 18,
            "Item": 15,
            "Quantity": 15,
            "Borrow Date": 13,
            "Return Date": 13,
            "Status": 12
        }

        for widget in table_frame.winfo_children():
            widget.destroy()

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
                anchor="center"
            )
            heading.grid(
                row=0,
                column=column_index,
                sticky="nsew"
            )

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
                pady=15
            )
            empty_label.grid(
                row=1,
                column=0,
                columnspan=len(columns),
                sticky="nsew"
            )
            return

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
                    anchor="center"
                )
                cell.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew"
                )

    def create_download_button(self, parent):
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

    def show_records(self):
        self.clear_content()

        self.page_title(
            "Borrowing Records",
            "View all borrowed and returned items.",
            action=self.create_download_button
        )

        container = self.create_container(
            self.content_frame
        )
        container.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=(5, 25)
        )

        self.create_bordered_table(
            container,
            "records"
        )

        self.populate_bordered_table(
            self.records_table_frame,
            self.records
        )

    def load_pil_font(self, size, bold=False):
        from PIL import ImageFont

        if bold:
            names = ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
        else:
            names = ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]

        for name in names:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue

        return ImageFont.load_default()

    def render_records_pages(self, rows_per_page):
        from PIL import Image, ImageDraw

        col_widths = [260, 260, 220, 130, 190, 190, 150]
        margin = 60
        table_width = sum(col_widths)
        page_width = table_width + margin * 2
        top = 190
        header_h = 70
        row_h = 64
        bottom = 90

        title_font = self.load_pil_font(46, bold=True)
        sub_font = self.load_pil_font(24)
        head_font = self.load_pil_font(24, bold=True)
        cell_font = self.load_pil_font(22)

        rows_per_page = max(1, rows_per_page)
        chunks = [
            self.records[i:i + rows_per_page]
            for i in range(0, len(self.records), rows_per_page)
        ]
        total_pages = len(chunks)
        rows_for_height = rows_per_page if total_pages > 1 else len(chunks[0])

        def draw_centered(draw, text, box, font, fill):
            x, y, w, h = box
            text = str(text)
            bbox = draw.textbbox((0, 0), text, font=font)

            while (bbox[2] - bbox[0]) > w - 20 and len(text) > 1:
                text = text[:-2] + "…" if not text.endswith("…") else text[:-2] + "…"
                bbox = draw.textbbox((0, 0), text, font=font)

            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(
                (x + (w - tw) / 2 - bbox[0], y + (h - th) / 2 - bbox[1]),
                text, font=font, fill=fill,
            )

        pages = []

        for page_no, chunk in enumerate(chunks, start=1):
            page_height = top + header_h + row_h * rows_for_height + bottom
            image = Image.new("RGB", (page_width, page_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            draw.text((margin, 50), "Borrowing Records", font=title_font, fill="#123A8C")
            draw.text(
                (margin, 115),
                f"Borrowise | Generated {datetime.now().strftime('%B %d, %Y %I:%M %p')}",
                font=sub_font, fill="#6689A8",
            )

            x = margin
            for name, w in zip(self.TABLE_COLUMNS, col_widths):
                draw.rectangle([x, top, x + w, top + header_h], fill="#DDF1FC", outline="#A8C5DF", width=2)
                draw_centered(draw, name, (x, top, w, header_h), head_font, "#123F87")
                x += w

            for r, record in enumerate(chunk):
                y = top + header_h + r * row_h
                fill = "#FFFFFF" if r % 2 == 0 else "#F2F8FD"
                x = margin
                for key, w in zip(self.TABLE_KEYS, col_widths):
                    draw.rectangle([x, y, x + w, y + row_h], fill=fill, outline="#C8DDF2", width=2)
                    draw_centered(draw, record.get(key, ""), (x, y, w, row_h), cell_font, "#123F87")
                    x += w

            footer_y = top + header_h + row_h * rows_for_height + 30
            draw.text(
                (margin, footer_y),
                f"Total records: {len(self.records)} Page {page_no} of {total_pages}",
                font=sub_font, fill="#6689A8",
            )

            pages.append(image)

        return pages

    def download_records(self, file_format):
        if not self.records:
            messagebox.showwarning("Borrowise", "There are no records to download yet.")
            return

        try:
            import PIL # noqa: F401
        except ImportError:
            messagebox.showerror(
                "Borrowise",
                "Downloading needs the Pillow library.\n\n"
                "Install it by running:\n pip install pillow",
            )
            return

        stamp = datetime.now().strftime("%Y%m%d_%H%M")

        if file_format == "pdf":
            path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Download Borrowing Records (PDF)",
                defaultextension=".pdf",
                initialfile=f"Borrowise_Records_{stamp}.pdf",
                filetypes=[("PDF file", "*.pdf")],
            )
        else:
            path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Download Borrowing Records (JPG)",
                defaultextension=".jpg",
                initialfile=f"Borrowise_Records_{stamp}.jpg",
                filetypes=[("JPG image", "*.jpg")],
            )

        if not path:
            return

        try:
            if file_format == "pdf":
                if not path.lower().endswith(".pdf"):
                    path += ".pdf"
                pages = self.render_records_pages(rows_per_page=15)
                pages[0].save(
                    path, "PDF", resolution=150.0,
                    save_all=True, append_images=pages[1:],
                )
            else:
                if not path.lower().endswith((".jpg", ".jpeg")):
                    path += ".jpg"
                page = self.render_records_pages(rows_per_page=len(self.records))[0]
                page.save(path, "JPEG", quality=95)
        except Exception as error:
            messagebox.showerror("Borrowise", f"Could not save the file.\n\n{error}")
            return

        messagebox.showinfo(
            "Borrowise", f"Records downloaded successfully!\n\n{os.path.basename(path)}"
        )

    def show_search(self):
        self.clear_content()

        self.page_title(
            "Search Records",
            "Search for borrowed or returned items."
        )

        search_container = self.create_container(
            self.content_frame
        )
        search_container.pack(
            fill="x",
            padx=45,
            pady=(5, 15)
        )

        search_frame = tk.Frame(
            search_container,
            bg="#F8FCFF"
        )
        search_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            search_frame,
            text="Search by:",
            font=("Arial", 12, "bold"),
            fg=self.text_blue,
            bg="#F8FCFF"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.search_combo = ttk.Combobox(
            search_frame,
            values=[
                "ID Number",
                "Name",
                "Item",
                "Quantity",
                "Status",
                "Borrow Date",
                "Return Date"
            ],
            state="readonly",
            style="Borrowise.TCombobox",
            width=15
        )
        self.search_combo.current(0)
        self.search_combo.pack(
            side="left",
            padx=(0, 10)
        )

        search_input_container = tk.Frame(
            search_frame,
            bg="#FFFFFF",
            highlightbackground=self.line_color,
            highlightthickness=2
        )
        search_input_container.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.search_entry = tk.Entry(
            search_input_container,
            font=("Arial", 12),
            bg="#FFFFFF",
            fg="#8AA2BD",
            relief="flat",
            bd=0
        )
        self.search_entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.search_entry.insert(
            0,
            "Enter keyword..."
        )

        self.search_entry.bind(
            "<FocusIn>",
            self.clear_search_placeholder
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_records()
        )

        tk.Button(
            search_frame,
            text="🔍Search",
            font=("Arial", 12, "bold"),
            fg="#FFFFFF",
            bg=self.blue,
            activebackground="#087DDC",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.search_records
        ).pack(
            side="left"
        )

        results_container = self.create_container(
            self.content_frame
        )
        results_container.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=(0, 25)
        )

        self.create_bordered_table(
            results_container,
            "search"
        )

        self.display_search_results(
            self.records
        )

    def clear_search_placeholder(self, event):
        if self.search_entry.get() == "Enter keyword...":
            self.search_entry.delete(
                0,
                tk.END
            )
            self.search_entry.config(
                fg=self.text_blue
            )

    def search_records(self):
        keyword = self.search_entry.get().strip().lower()

        if keyword == "enter keyword...":
            keyword = ""

        if not keyword:
            self.display_search_results(self.records)
            return

        search_type = self.search_combo.get()

        field_mapping = {
            "ID Number": "borrower_id",
            "Name": "name",
            "Item": "item",
            "Quantity": "quantity",
            "Status": "status",
            "Borrow Date": "borrow_date",
            "Return Date": "return_date"
        }

        field = field_mapping.get(search_type)

        if field is None:
            self.display_search_results([])
            return

        results = []

        for record in self.records:
            value = str(
                record.get(field, "")
            ).strip().lower()

            if keyword in value:
                results.append(record)

        self.display_search_results(results)

    def display_search_results(self, results):
        if not hasattr(self, "search_table_frame"):
            return

        self.populate_bordered_table(
            self.search_table_frame,
            results
        )

    def logout(self):
        answer = messagebox.askyesno(
            "Logout", "Are you sure you want to logout?"
        )
        if answer:
            self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = BorrowiseApp(root)
    root.mainloop()
