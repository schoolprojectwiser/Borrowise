# ==========================================================
# validators.py
# Input validation: password rules, ID Number typing rules
# and date typing rules.
# ==========================================================

from config import (
    ID_MAX_DIGITS,
    ID_MAX_HYPHENS,
    PASSWORD_MAX,
    PASSWORD_MIN,
    PASSWORD_PATTERN,
)


def check_new_password(pwd):
    # MAIN COMMENT: Checks a NEW password against the password rules
    # (length 8-13, letters/numbers/_/- only).
    # Returns an error message string, or None when the password is valid.

    # Rule 1: length must be inside the allowed range
    if len(pwd) < PASSWORD_MIN or len(pwd) > PASSWORD_MAX:
        return f"Password must be {PASSWORD_MIN} to {PASSWORD_MAX} characters long."

    # Rule 2: only allowed characters
    if not PASSWORD_PATTERN.match(pwd):
        return "Password may only contain letters, numbers, \"_\" and \"-\"."

    # No problems found
    return None


class ValidationMixin:
    """Typing-validation methods used by Entry widgets."""

    def init_validation(self):
        # MAIN COMMENT: Registers the Tk validation callbacks so Entry widgets
        # can use them through validate="key" / validatecommand=...

        # Placeholder texts that must be allowed in ID entries
        self.id_placeholders = {"ID Number", "e.g., 03-01-2627-001668"}

        # "%P" = the value the entry WOULD have if the key is accepted
        self.vcmd_id = (self.root.register(self.validate_id_input), "%P")
        self.vcmd_date = (self.root.register(self.validate_date_input), "%P")

    def validate_id_input(self, proposed):
        # MAIN COMMENT: Allows only digits and hyphens in an ID Number,
        # up to 14 digits and 3 hyphens. Placeholder text is always allowed.

        if proposed in self.id_placeholders:
            return True

        digits = 0
        hyphens = 0

        # Count each character; reject anything that is not a digit or "-"
        for ch in proposed:
            if ch.isdigit() and ch.isascii():
                digits += 1
            elif ch == "-":
                hyphens += 1
            else:
                return False

        return digits <= ID_MAX_DIGITS and hyphens <= ID_MAX_HYPHENS

    def validate_date_input(self, proposed):
        # MAIN COMMENT: Allows only digits and hyphens in a date entry,
        # with a maximum of 10 characters (MM-DD-YYYY).

        if len(proposed) > 10:
            return False
        return all((ch.isdigit() and ch.isascii()) or ch == "-" for ch in proposed)
