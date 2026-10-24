# ==========================================================
# calendar_picker.py
# Popup calendar used to pick a date for a date entry.
# ==========================================================

import calendar
import tkinter as tk
from datetime import datetime

from config import DATE_FORMAT


class CalendarPickerMixin:
    """Date picker popup."""

    def open_calendar(self, target_entry, allow_past=False):
        # MAIN COMMENT: Opens a month calendar under the given entry. The
        # clicked day is written into the entry as MM-DD-YYYY. Past days are
        # disabled unless allow_past=True.

        # Start on the date already typed, or today if it is invalid
        try:
            current = datetime.strptime(target_entry.get().strip(), DATE_FORMAT)
        except ValueError:
            current = datetime.now()

        today = datetime.now().date()
        selected = current.date()
        state = {"year": current.year, "month": current.month}  # month being shown

        # ----- window (placed right under the entry) -----
        popup = tk.Toplevel(self.root)
        popup.title("Select Date")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.transient(self.root)

        width, height = 340, 370
        x = target_entry.winfo_rootx()
        y = target_entry.winfo_rooty() + target_entry.winfo_height() + 10
        popup.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")
        popup.grab_set()
        popup.bind("<Escape>", lambda e: popup.destroy())

        # ----- header: previous month / title / next month -----
        header = tk.Frame(popup, bg="white")
        header.pack(fill="x", padx=15, pady=(15, 8))

        title_label = tk.Label(
            header, text="", font=("Arial", 14, "bold"), fg=self.dark_blue, bg="white"
        )

        def change_month(delta):
            # Moves the calendar one month back (-1) or forward (+1)
            month = state["month"] + delta
            year = state["year"]
            if month < 1:
                month, year = 12, year - 1
            elif month > 12:
                month, year = 1, year + 1
            state["month"], state["year"] = month, year
            draw_days()

        tk.Button(
            header, text="◀", font=("Arial", 12, "bold"), fg=self.blue, bg="white",
            activebackground="#E8F4FF", relief="flat", bd=0, cursor="hand2",
            command=lambda: change_month(-1),
        ).pack(side="left")
        title_label.pack(side="left", expand=True)
        tk.Button(
            header, text="▶", font=("Arial", 12, "bold"), fg=self.blue, bg="white",
            activebackground="#E8F4FF", relief="flat", bd=0, cursor="hand2",
            command=lambda: change_month(1),
        ).pack(side="right")

        # ----- weekday names (Su Mo Tu ...) -----
        grid = tk.Frame(popup, bg="white")
        grid.pack(padx=15)

        day_names = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        for col, name in enumerate(day_names):
            tk.Label(
                grid, text=name, font=("Arial", 10, "bold"), fg=self.text_gray,
                bg="white", width=4, height=2,
            ).grid(row=0, column=col)

        days_frame = tk.Frame(popup, bg="white")
        days_frame.pack(padx=15)

        def pick(year, month, day):
            # Writes the chosen date into the entry and closes the popup
            target_entry.delete(0, tk.END)
            target_entry.insert(0, datetime(year, month, day).strftime(DATE_FORMAT))
            popup.destroy()

        def draw_days():
            # Redraws the day buttons for the month in "state"
            for widget in days_frame.winfo_children():
                widget.destroy()

            year, month = state["year"], state["month"]
            title_label.config(text=f"{calendar.month_name[month]} {year}")

            # Weeks start on Sunday (firstweekday=6)
            weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)

            for row, week in enumerate(weeks):
                for col, day in enumerate(week):
                    # Empty cell (day belongs to another month)
                    if day == 0:
                        tk.Label(days_frame, text="", bg="white", width=4, height=2).grid(
                            row=row, column=col
                        )
                        continue

                    this_date = datetime(year, month, day).date()
                    is_past = this_date < today and not allow_past
                    is_selected = this_date == selected

                    # Choose colors: past (gray) / selected (blue) / today / normal
                    if is_past:
                        fg, bg = "#B7C6D6", "white"
                    elif is_selected:
                        fg, bg = "white", self.blue
                    elif this_date == today:
                        fg, bg = self.dark_blue, "#DDF1FC"
                    else:
                        fg, bg = self.dark_blue, "white"

                    tk.Button(
                        days_frame,
                        text=str(day),
                        font=("Arial", 10, "bold" if is_selected else "normal"),
                        fg=fg,
                        bg=bg,
                        activebackground="#B9DDF5",
                        activeforeground=self.dark_blue,
                        relief="flat",
                        bd=0,
                        width=4,
                        height=2,
                        state="disabled" if is_past else "normal",
                        cursor="arrow" if is_past else "hand2",
                        command=lambda y=year, m=month, d=day: pick(y, m, d),
                    ).grid(row=row, column=col, padx=1, pady=1)

        # ----- footer: Today / Close -----
        footer = tk.Frame(popup, bg="white")
        footer.pack(side="bottom", fill="x", padx=15, pady=12)

        def go_today():
            # Picks today's date directly
            pick(today.year, today.month, today.day)

        tk.Button(
            footer, text="Today", font=("Arial", 10, "bold"), fg=self.blue, bg="#E8F4FF",
            activebackground="#CBE9FA", relief="flat", bd=0, padx=16, pady=5,
            cursor="hand2", command=go_today,
        ).pack(side="left")

        tk.Button(
            footer, text="Close", font=("Arial", 10, "bold"), fg=self.text_blue, bg="#F0F4F8",
            activebackground="#DCE5EE", relief="flat", bd=0, padx=16, pady=5,
            cursor="hand2", command=popup.destroy,
        ).pack(side="right")

        draw_days()
