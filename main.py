# ==========================================================
# main.py
# Entry point of Borrowise. Run this file:  python main.py
#
# The app class only joins the feature modules together.
# Each feature lives in its own file and does not depend on
# the code of other features (they only share the app state
# such as self.root, self.records and the color attributes).
# ==========================================================

import tkinter as tk

from borrow import BorrowMixin
from calendar_picker import CalendarPickerMixin
from config import SECURITY_QUESTIONS
from create_account import CreateAccountMixin
from dashboard import DashboardMixin
from download import DownloadMixin
from forgot_password import ForgotPasswordMixin
from form_rows import FormRowsMixin
from icons import IconsMixin
from lockout import LockoutMixin
from login import LoginMixin
from logout import LogoutMixin
from profile_page import ProfileMixin
from records import RecordsMixin
from return_item import ReturnItemMixin
from search import SearchMixin
from security_answer import SecurityAnswerMixin
from theme import ThemeMixin
from ui_helpers import UIHelpersMixin
from validators import ValidationMixin


class BorrowiseApp(
    ThemeMixin,
    ValidationMixin,
    UIHelpersMixin,
    FormRowsMixin,
    IconsMixin,
    LoginMixin,
    LockoutMixin,
    SecurityAnswerMixin,
    ForgotPasswordMixin,
    CreateAccountMixin,
    LogoutMixin,
    DashboardMixin,
    ProfileMixin,
    CalendarPickerMixin,
    BorrowMixin,
    ReturnItemMixin,
    RecordsMixin,
    DownloadMixin,
    SearchMixin,
):

    def __init__(self, root):
        # MAIN COMMENT: Sets up the window, the temporary admin account,
        # colors, validation and styles, then opens the login screen.

        self.root = root
        self.root.title("Borrowise")

        # ----- window settings (full screen) -----
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # ----- temporary login account -----
        # Security answer for the admin account is: blue
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

        # ----- lockout state -----
        self.failed_attempts = 0
        self.lockout_until = 0
        self.lockout_popup = None
        self.lockout_message = "Incorrect ID Number or password."

        # ----- borrowing records (in memory) -----
        self.records = []

        # ----- feature setup -----
        self.init_colors()
        self.init_validation()
        self.init_styles()

        self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = BorrowiseApp(root)
    root.mainloop()

