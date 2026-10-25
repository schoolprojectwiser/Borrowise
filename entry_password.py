# ==========================================================
# forgot_password.py
# "Forgot password?" popup: reset the password of an account.
# The user must answer the account's security question before
# the new password is applied.
# ==========================================================

import time
import tkinter as tk
from tkinter import messagebox

from config import PASSWORD_HINT, SECURITY_QUESTIONS
from password_entry import PasswordEntry
from validators import check_new_password


class ForgotPasswordMixin:
    """Reset-password popup + security verification step."""

    def open_forgot_password_window(self):
        # MAIN COMMENT: Opens the Reset Password popup (ID Number + new
        # password). When RESET PASSWORD is pressed, the security question
        # popup opens; the password only changes if the answer is correct.

        # ----- window -----
        popup = tk.Toplevel(self.root)
        popup.title("Forgot Password")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        self.center_popup(popup, 420, 400)
        popup.grab_set()

        tk.Label(
            popup, text="Reset Password", font=("Arial", 18, "bold"),
            fg=self.dark_blue, bg="white",
        ).pack(pady=(25, 15))

        # ----- ID Number field -----
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

        # ----- New password field (restricted) -----
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
            # Validates the inputs, then asks the security question
            acc_id = f_id.get().strip()
            new_pass = f_pass.get().strip()

            if acc_id == id_placeholder:
                acc_id = ""

            # All fields are required
            if not acc_id or not new_pass:
                messagebox.showwarning(
                    "Warning", "Please fill in all fields.", parent=popup
                )
                return

            # New password must follow the rules
            error = check_new_password(new_pass)
            if error:
                messagebox.showerror("Error", error, parent=popup)
                return

            account = self.registered_accounts.get(acc_id)

            if not account:
                messagebox.showerror(
                    "Error", "ID Number is incorrect or does not exist.", parent=popup,
                )
                return

            # Still locked out from earlier wrong attempts -> show the timer
            if time.time() < self.lockout_until:
                popup.destroy()
                self.show_lockout_popup()
                return

            # Everything is fine so far -> ask the security question
            self.open_reset_security_popup(popup, account, new_pass)

        # ----- Reset button -----
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

    def open_reset_security_popup(self, parent_popup, account, new_pass):
        # MAIN COMMENT: Asks the account's security question before the
        # password is changed. Correct answer -> password is saved.
        # Wrong answer -> counts as a failed attempt (lockout warning popup).
        # Cancel -> goes back to the Reset Password window.

        question = account.get("security_question", SECURITY_QUESTIONS[0])
        correct_answer = account.get("security_answer", "")

        # ----- window -----
        popup = tk.Toplevel(self.root)
        popup.title("Security Verification")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(parent_popup)
        self.center_popup(popup, 440, 400)
        popup.grab_set()

        def cancel():
            # Close this popup and give control back to the reset window
            popup.destroy()
            parent_popup.grab_set()

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
            popup, text="Answer your security question to reset the password.",
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
                messagebox.showwarning(
                    "Security Verification", "Please enter your answer.", parent=popup
                )
                return

            if typed == saved:
                # Correct -> now the password can really be changed
                account["password"] = new_pass
                self.save_data()
                popup.destroy()
                messagebox.showinfo(
                    "Success", "Password has been reset successfully!",
                    parent=parent_popup,
                )
                parent_popup.destroy()
            else:
                # Wrong -> failed attempt + lockout warning popup
                popup.destroy()
                parent_popup.destroy()
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
