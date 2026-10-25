# ==========================================================
# logout.py
# Logout confirmation.
# ==========================================================

from tkinter import messagebox


class LogoutMixin:
    """Logout feature."""

    def logout(self):
        # MAIN COMMENT: Asks the user to confirm, then returns to the
        # login screen.
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if answer:
            self.show_login()
