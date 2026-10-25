\# ==========================================================
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

# Item list for the Borrow page, grouped by category.
ITEM_PLACEHOLDER = "Select item"

ITEM_CATEGORIES = {
    "Education and Media": [
        "Laptop", "Projector", "Keyboard", "Mouse",
        "Calculator", "Monitor", "Speaker",
    ],
    "Household": [
        "Electric Fan", "Vacuum Cleaner", "Rice Cooker", "Blender",
        "Cooler", "Air Fryer", "Microwave", "Pressure Cooker", "Steamer",
    ],
    "Tools and Electronics": [
        "Electric Drill", "Hammer", "Screwdriver Set", "Wrench Set",
        "Measuring Tape", "Pliers", "Extension Cord", "Hand Saw",
        "Hacksaw", "Allen Key Set", "Clamps", "Vise Grips", "Heat Gun",
        "Soldering Iron", "Shovel", "Ladder",
    ],
    "Sports": [
        "Basketball", "Volleyball", "Football", "Net",
        "Badminton Racket Set", "Tennis Rackets", "Tennis Paddles",
        "Ping Pong Table", "Camping Tent",
    ],
}

# Category titles are shown in the dropdown as unselectable headers.
ITEM_HEADERS = {f"── {name} ──" for name in ITEM_CATEGORIES}

ITEM_CHOICES = [ITEM_PLACEHOLDER]
for _name, _items in ITEM_CATEGORIES.items():
    ITEM_CHOICES.append(f"── {_name} ──")
    ITEM_CHOICES.extend(_items)
