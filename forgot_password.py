# ==========================================================
# forgot_password.py
# "Forgot password?" popup: reset the password of an account.
# ==========================================================

import tkinter as tk
from tkinter import messagebox

from config import PASSWORD_HINT
from password_entry import PasswordEntry
from validators import check_new_password


class ForgotPasswordMixin:
    """Reset-password popup."""

    def open_forgot_password_window(self):
        # MAIN COMMENT: Opens the Reset Password popup (ID Number + new
        # password) and applies the new password if the account exists.

        # ----- window -----
        popup = tk.Toplevel(self.root)
        popup.title("Forgot Password")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        self.center_popup(popup, 420, 480)
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
            # Validates the inputs and saves the new password
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

            if account:
                account["password"] = new_pass
                messagebox.showinfo(
                    "Success", "Password has been reset successfully!", parent=popup,
                )
                popup.destroy()
            else:
                messagebox.showerror(
                    "Error", "ID Number is incorrect or does not exist.", parent=popup,
                )

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
