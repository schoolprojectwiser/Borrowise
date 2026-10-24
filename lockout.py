# ==========================================================
# lockout.py
# Failed-attempt counter + the "Login Warning" countdown popup.
# Used by BOTH the password step and the security-answer step.
# ==========================================================

import math
import time
import tkinter as tk

from config import LOCKOUT_SECONDS


class LockoutMixin:
    """Lockout logic after incorrect login attempts."""

    def register_failed_attempt(self, reason="Incorrect ID Number or password."):
        # MAIN COMMENT: Records one failed login attempt, starts the lockout
        # timer (longer each time) and shows the warning popup.

        self.failed_attempts += 1

        # Pick the lockout length (the last value repeats after the 4th)
        seconds = LOCKOUT_SECONDS[min(self.failed_attempts, len(LOCKOUT_SECONDS)) - 1]
        self.lockout_until = time.time() + seconds
        self.lockout_message = reason

        # Clear the typed password on the login screen
        self.password_field.clear()
        self.show_lockout_popup()

    def show_lockout_popup(self):
        # MAIN COMMENT: Shows a modal popup with a countdown. The OK button
        # stays disabled until the lockout time is over.

        # Reuse the popup if it is already open
        if self.lockout_popup is not None:
            try:
                if self.lockout_popup.winfo_exists():
                    self.lockout_popup.lift()
                    return
            except tk.TclError:
                pass

        warning_no = min(self.failed_attempts, len(LOCKOUT_SECONDS))

        # ----- window -----
        popup = tk.Toplevel(self.root)
        self.lockout_popup = popup
        popup.title("Login Warning")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)
        popup.protocol("WM_DELETE_WINDOW", lambda: None)  # cannot close while locked
        self.center_popup(popup, 460, 340)
        popup.grab_set()

        # ----- warning icon + title -----
        tk.Label(
            popup, text="⚠️", font=("Segoe UI Emoji", 36), fg="#E74C3C", bg="white",
        ).pack(pady=(20, 0))

        tk.Label(
            popup,
            text=f"Warning {warning_no} of {len(LOCKOUT_SECONDS)}",
            font=("Arial", 18, "bold"),
            fg="#A93226",
            bg="white",
        ).pack(pady=(5, 0))

        # ----- message -----
        if warning_no >= len(LOCKOUT_SECONDS):
            message = "Too many incorrect attempts.\nYou are locked out for 5 minutes."
        else:
            message = getattr(self, "lockout_message", "Incorrect ID Number or password.")

        tk.Label(
            popup, text=message, font=("Arial", 11), fg=self.text_blue,
            bg="white", justify="center",
        ).pack(pady=(8, 8))

        # ----- countdown -----
        countdown_label = tk.Label(
            popup, text="", font=("Arial", 26, "bold"), fg=self.dark_blue, bg="white",
        )
        countdown_label.pack()

        tk.Label(
            popup, text="Please wait before trying again.",
            font=("Arial", 10), fg=self.text_gray, bg="white",
        ).pack(pady=(0, 10))

        # ----- OK button (disabled until time is up) -----
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
            # Turns seconds into MM:SS text
            return f"{secs // 60:02d}:{secs % 60:02d}"

        def tick():
            # Updates the countdown 4 times per second
            remaining = max(0, math.ceil(self.lockout_until - time.time()))
            countdown_label.config(text=format_time(remaining))

            if remaining > 0:
                popup.after(250, tick)
            else:
                # Time is over: enable OK and allow closing the window
                ok_button.config(
                    text="OK", state="normal", bg=self.blue, cursor="hand2",
                    activebackground="#087DDC", activeforeground="white",
                )
                popup.protocol("WM_DELETE_WINDOW", popup.destroy)

        tick()
