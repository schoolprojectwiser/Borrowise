# ==========================================================
# create_account.py
# "Create new account" popup: register a new user with a
# security question and answer.
# ==========================================================

import tkinter as tk
from tkinter import messagebox

from config import QUESTION_PLACEHOLDER
from password_entry import PasswordEntry
from validators import check_new_password


class CreateAccountMixin:
    """Account registration popup."""

    def open_create_account_window(self):
        # MAIN COMMENT: Opens the Create New Account popup and saves the new
        # account (ID, name, security question/answer, password) in memory.

        # ----- window -----
        popup = tk.Toplevel(self.root)
        popup.title("Create New Account")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        self.center_popup(popup, 440, 700)
        popup.grab_set()

        tk.Label(
            popup, text="Create New Account", font=("Arial", 18, "bold"),
            fg=self.dark_blue, bg="white",
        ).pack(pady=(20, 10))

        # ----- ID Number -----
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

        # ----- Full name -----
        self.popup_label(popup, "Full Name:")
        name_entry = tk.Entry(
            popup, font=("Arial", 12), bg="#F5FAFF", relief="solid", bd=1
        )
        name_entry.pack(fill="x", padx=35, pady=(3, 10), ipady=4)

        # ----- Security question + answer -----
        self.popup_label(popup, "Security Question:")
        question_combo = self.make_question_combo(popup)
        question_combo.pack(fill="x", padx=35, pady=(3, 10), ipady=3)

        self.popup_label(popup, "Security Answer:")
        answer_entry = tk.Entry(
            popup, font=("Arial", 12), bg="#F5FAFF", relief="solid", bd=1
        )
        answer_entry.pack(fill="x", padx=35, pady=(3, 10), ipady=4)

        # ----- Password + confirm password -----
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
            # Validates every field, then stores the new account
            new_id = id_entry.get().strip()
            fullname = name_entry.get().strip()
            question = question_combo.get()
            answer = answer_entry.get().strip()
            pwd = p_entry.get()
            cpwd = cp_entry.get()

            # Every field is required
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

            # Password rules
            error = check_new_password(pwd)
            if error:
                messagebox.showerror("Error", error, parent=popup)
                return

            # Both passwords must match
            if pwd != cpwd:
                messagebox.showerror("Error", "Passwords do not match!", parent=popup)
                return

            # ID Number must be unique
            if new_id in self.registered_accounts:
                messagebox.showerror(
                    "Error", "An account with this ID Number already exists!",
                    parent=popup,
                )
                return

            # Save the account
            self.registered_accounts[new_id] = {
                "password": pwd,
                "fullname": fullname,
                "security_question": question,
                "security_answer": answer,
            }

            messagebox.showinfo(
                "Success", "Account created successfully! You can now log in.",
                parent=popup,
            )
            popup.destroy()

        # ----- Create button -----
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

        # ----- "Already have an account? Log in" link -----
        link_frame = tk.Frame(popup, bg="white")
        link_frame.pack(pady=10)

        tk.Label(
            link_frame, text="Already have an account?",
            font=("Arial", 9), fg="gray", bg="white",
        ).pack(side="left")

        login_link = tk.Label(
            link_frame, text=" Log in", font=("Arial", 9, "bold"),
            fg=self.blue, bg="white", cursor="hand2",
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: popup.destroy())
