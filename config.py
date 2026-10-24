# ==========================================================
# config.py
# Shared constants used by the whole Borrowise app.
# No UI code lives here, only settings.
# ==========================================================

import re

# Questions the user can choose from when creating an account
SECURITY_QUESTIONS = [
    "What is your pet name?",
    "What is your favorite food?",
    "What is your Mother's maiden name?",
    "What is your favorite color?",
    "What is your date of birth?",
]

# Text shown in the combobox before the user picks a question
QUESTION_PLACEHOLDER = "Select security question"

# Lockout (seconds) after the 1st, 2nd, 3rd and 4th incorrect attempts
LOCKOUT_SECONDS = [5, 15, 30, 300]

# ID Number limits (digits and hyphens)
ID_MAX_DIGITS = 14
ID_MAX_HYPHENS = 3

# Password rules for NEW passwords (create account / reset password)
PASSWORD_MIN = 8
PASSWORD_MAX = 13
PASSWORD_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
PASSWORD_HINT = "8-13 characters: letters, numbers, \"_\" and \"-\" only"

# Date format used everywhere (MM-DD-YYYY)
DATE_FORMAT = "%m-%d-%Y"
