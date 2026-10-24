# ==========================================================
# icons.py
# Small icons drawn with Tkinter canvases (no image files).
# ==========================================================

import tkinter as tk


class IconsMixin:
    """Canvas-drawn icons used on forms."""

    def create_card_icon(self, parent, x, y):
        # MAIN COMMENT: Draws an ID-card icon centered at (x, y) inside parent.
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        color = "#557AA7"

        canvas.create_rectangle(3, 8, 37, 32, outline=color, width=3)   # card body
        canvas.create_oval(8, 13, 17, 22, fill=color, outline="")        # head
        canvas.create_arc(6, 22, 20, 36, start=0, extent=180, fill=color, outline="")  # shoulders
        canvas.create_line(23, 15, 33, 15, fill=color, width=2)          # text lines
        canvas.create_line(23, 21, 33, 21, fill=color, width=2)
        canvas.create_line(23, 27, 30, 27, fill=color, width=2)

    def create_question_icon(self, parent, x, y):
        # MAIN COMMENT: Draws a circled question-mark icon centered at (x, y).
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        color = "#557AA7"

        canvas.create_oval(5, 5, 35, 35, outline=color, width=3)
        canvas.create_text(20, 20, text="?", font=("Arial", 15, "bold"), fill=color)

    def create_key_icon(self, parent, x, y):
        # MAIN COMMENT: Draws a key icon centered at (x, y).
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        color = "#557AA7"

        canvas.create_oval(5, 10, 21, 26, outline=color, width=3)   # key head
        canvas.create_line(21, 18, 36, 18, fill=color, width=3)     # shaft
        canvas.create_line(30, 18, 30, 25, fill=color, width=3)     # teeth
        canvas.create_line(35, 18, 35, 24, fill=color, width=3)

    def create_lock_icon(self, parent, x, y):
        # MAIN COMMENT: Draws a padlock icon centered at (x, y).
        canvas = tk.Canvas(
            parent, width=40, height=40, bg="white", highlightthickness=0
        )
        canvas.place(x=x - 20, y=y - 20)
        lock_color = "#557AA7"

        # shackle (top curve + two legs)
        canvas.create_arc(
            10, 4, 30, 24,
            start=0, extent=180, style="arc", outline=lock_color, width=4,
        )
        canvas.create_line(10, 14, 10, 19, fill=lock_color, width=4)
        canvas.create_line(30, 14, 30, 19, fill=lock_color, width=4)
        # body
        canvas.create_rectangle(8, 17, 32, 36, fill=lock_color, outline="")
        # keyhole
        canvas.create_oval(18, 21, 22, 25, fill="white", outline="")
        canvas.create_rectangle(19, 24, 21, 29, fill="white", outline="")
