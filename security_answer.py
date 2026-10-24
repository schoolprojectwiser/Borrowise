# ==========================================================
# security_answer.py
# NEW FEATURE: after the ID Number and password are correct,
# the user must answer their security question before the
# dashboard opens.
# ==========================================================

import tkinter as tk
from tkinter import messagebox

from config import SECURITY_QUESTIONS
from password_entry import PasswordEntry


class SecurityAnswerMixin:
    """Second login step: security answer verification."""

    def show_security_answer_popup(self, id_num, account):
        # MAIN COMMENT: Opens a modal popup that asks the account's security
        # question. Correct answer -> dashboard opens. Wrong answer -> counts
        # as a failed attempt (lockout). Cancel -> back to the login screen.

        question = account.get("security_question", SECURITY_QUESTIONS[0])
        correct_answer = account.get("security_answer", "")

        # ----- window -----
        popup = tk.Toplevel(self.root)
        popup.title("Security Verification")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        self.center_popup(popup, 440, 480)
        popup.grab_set()

        def cancel():
            # Close the popup and return to the login screen
            popup.destroy()
            self.password_field.clear()

        popup.protocol("WM_DELETE_WINDOW", cancel)
        popup.bind("<Escape>", lambda e: cancel())

        # ----- header -----
        tk.Label(
            popup, text="🔐", font=("Segoe UI Emoji", 32), bg="white",
        ).pack(pady=(20, 0))

        tk.Label(
            popup, text="Security Verification",
            font=("Arial", 18, "bold"), fg=self.dark_blue, bg="white",
        ).pack(pady=(5, 5))

        tk.Label(
            popup, text="Answer your security question to continue.",
            font=("Arial", 10), fg=self.text_gray, bg="white",
        ).pack(pady=(0, 15))

        # ----- the question (read-only text) -----
        self.popup_label(popup, "Security Question:")
        tk.Label(
            popup,
            text=question,
            font=("Arial", 12, "bold"),
            fg=self.dark_blue,
            bg="#E8F4FF",
            anchor="w",
            padx=10,
            pady=8,
        ).pack(fill="x", padx=35, pady=(3, 12))

        # ----- the answer (hidden by default, eye icon to reveal) -----
        self.popup_label(popup, "Security Answer:")
        answer_field = PasswordEntry(
            popup,
            placeholder="Enter your answer",
            bg="#F5FAFF",
            font=("Arial", 12),
            border_color="#7F9DB9",
            border_width=1,
            ipady=5,
        )
        answer_field.pack(fill="x", padx=35, pady=(3, 15))

        def verify():
            # Compares the typed answer with the saved answer
            # (ignores capital letters and extra spaces)
            typed = answer_field.get().strip().lower()
            saved = str(correct_answer).strip().lower()

            if not typed:
                self.show_security_error(popup, "Please enter your answer.")
                return

            if typed == saved:
                popup.destroy()
                self.complete_login(id_num, account)
            else:
                # Wrong answer counts as a failed login attempt
                popup.destroy()
                self.register_failed_attempt("Incorrect security answer.")

        # ----- buttons -----
        tk.Button(
            popup, text="VERIFY", font=("Arial", 11, "bold"), fg="white",
            bg=self.blue, activebackground="#087DDC", activeforeground="white",
            relief="flat", cursor="hand2", command=verify,
        ).pack(fill="x", padx=35, ipady=10)

        tk.Button(
            popup, text="Cancel", font=("Arial", 10, "bold"), fg=self.text_blue,
            bg="#DCEFFC", activebackground="#CBE9FA", relief="flat",
            cursor="hand2", command=cancel,
        ).pack(fill="x", padx=35, pady=(8, 0), ipady=5)

        # Pressing Enter inside the popup verifies the answer
        popup.bind("<Return>", lambda e: verify())

    def show_security_error(self, popup, text):
        # MAIN COMMENT: Shows a warning box over the security popup
        # (used when the answer field is empty).
        messagebox.showwarning("Security Verification", text, parent=popup)

    def complete_login(self, id_num, account):
        # MAIN COMMENT: Final login step. Resets the failed-attempt counter,
        # saves who is logged in and opens the dashboard.

        self.failed_attempts = 0
        self.lockout_until = 0

        self.current_user = {
            "id": id_num,
            "fullname": account.get("fullname", id_num),
            "security_question": account.get("security_question", SECURITY_QUESTIONS[0]),
        }

        self.root.unbind("<Return>")  # stop the Enter-to-login shortcut
        self.show_dashboard()
