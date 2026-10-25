# ==========================================================
# password_entry.py
# Reusable password input widget with a placeholder and an
# eye icon (closed = hidden, open = visible).
# ==========================================================

import tkinter as tk

from config import PASSWORD_MAX


class PasswordEntry(tk.Frame):
    """Entry with a placeholder and a drawn eye icon.
    Closed eye = password hidden (dots)
    Open eye = password visible
    Only the icon changes when clicked.

    restrict=True -> max 13 characters, only letters/numbers/_/-,
                      and the first letter is automatically uppercase.
    allow_special=True -> max 13 characters, letters/numbers/special
                      characters allowed (no spaces), no auto-uppercase.
                      Used by the login password field."""

    def __init__(
        self,
        parent,
        placeholder="Password",
        bg="white",
        fg="#123F87",
        placeholder_fg="#60799B",
        font=("Arial", 12),
        border_color=None,
        border_width=0,
        eye_color="#557AA7",
        ipady=0,
        restrict=False,
        allow_special=False,
    ):
        # MAIN COMMENT: Builds the widget: a frame holding the text entry
        # on the left and the eye canvas on the right.
        super().__init__(
            parent,
            bg=bg,
            highlightbackground=border_color or bg,
            highlightcolor=border_color or bg,
            highlightthickness=border_width,
        )

        # Remember the settings
        self.placeholder = placeholder
        self.bg = bg
        self.fg = fg
        self.placeholder_fg = placeholder_fg
        self.eye_color = eye_color
        self.hidden = True            # password starts hidden
        self.has_placeholder = True   # placeholder is showing at start
        self.restrict = restrict
        self.allow_special = allow_special

        # Eye icon (right side)
        self.eye = tk.Canvas(
            self, width=28, height=28, bg=bg, highlightthickness=0, cursor="hand2"
        )
        self.eye.pack(side="right", padx=(0, 6))
        self.eye.bind("<Button-1>", lambda e: self.toggle())

        # Key validation only when restrict or allow_special is on
        entry_options = {}
        if restrict or allow_special:
            entry_options["validate"] = "key"
            entry_options["validatecommand"] = (self.register(self._validate), "%P")

        # Text entry (left side)
        self.entry = tk.Entry(
            self,
            font=font,
            bd=0,
            relief="flat",
            bg=bg,
            fg=placeholder_fg,
            highlightthickness=0,
            insertbackground=fg,
            **entry_options,
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(8, 4), ipady=ipady)

        # Placeholder behaviour
        self.entry.bind("<FocusIn>", self._focus_in)
        self.entry.bind("<FocusOut>", self._focus_out)

        # Auto-uppercase the first letter in restricted mode
        if restrict:
            self.entry.bind("<KeyRelease>", self._auto_capitalize)

        self._show_placeholder()
        self._draw_eye()

    # ---------- restriction handling ----------
    def _validate(self, proposed):
        # MAIN COMMENT: Tk validation callback. Rejects keystrokes that would
        # make the password too long or contain forbidden characters.
        if self.has_placeholder:
            return True
        if len(proposed) > PASSWORD_MAX:
            return False
        if self.restrict:
            return all(ch.isascii() and (ch.isalnum() or ch in "_-") for ch in proposed)
        # allow_special: any printable ASCII character except space
        return all(ch.isascii() and ch.isprintable() and ch != " " for ch in proposed)

    def _auto_capitalize(self, event=None):
        # MAIN COMMENT: Turns the first typed letter into uppercase
        # while keeping the cursor where it was.
        if self.has_placeholder:
            return
        text = self.entry.get()
        if text and text[0].isalpha() and text[0].islower():
            pos = self.entry.index(tk.INSERT)
            self.entry.delete(0, 1)
            self.entry.insert(0, text[0].upper())
            self.entry.icursor(pos)

    # ---------- placeholder handling ----------
    def _show_placeholder(self):
        # MAIN COMMENT: Puts the gray placeholder text into the entry.
        self.has_placeholder = True
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=self.placeholder_fg, show="")

    def _focus_in(self, event=None):
        # MAIN COMMENT: When the user clicks the field, remove the placeholder
        # and switch to normal text color.
        if self.has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.fg)
            self.has_placeholder = False
            self._apply_show()

    def _focus_out(self, event=None):
        # MAIN COMMENT: When the user leaves an empty field, bring the
        # placeholder back.
        if not self.has_placeholder and self.entry.get() == "":
            self._show_placeholder()

    # ---------- eye handling ----------
    def _apply_show(self):
        # MAIN COMMENT: Shows dots when hidden, real text when visible.
        # The placeholder is never masked.
        if self.has_placeholder:
            self.entry.config(show="")
        else:
            self.entry.config(show="•" if self.hidden else "")

    def toggle(self):
        # MAIN COMMENT: Switches between hidden/visible password and
        # redraws the eye icon.
        self.hidden = not self.hidden
        self._apply_show()
        self._draw_eye()

    def _draw_eye(self):
        # MAIN COMMENT: Draws the eye icon. A slash through the eye means
        # the password is currently hidden.
        c = self.eye
        col = self.eye_color
        c.delete("all")

        # almond-shaped eye outline
        c.create_polygon(
            2, 14, 8, 8, 14, 6, 20, 8, 26, 14, 20, 20, 14, 22, 8, 20,
            smooth=True, fill="", outline=col, width=2,
        )
        # pupil
        c.create_oval(10, 10, 18, 18, fill=col, outline="")

        if self.hidden:
            # closed eye = slash through the icon
            c.create_line(5, 24, 24, 4, fill=self.bg, width=5)
            c.create_line(5, 24, 24, 4, fill=col, width=2)

    # ---------- public API ----------
    def get(self):
        # MAIN COMMENT: Returns the typed password ("" if only the
        # placeholder is showing).
        return "" if self.has_placeholder else self.entry.get()

    def clear(self):
        # MAIN COMMENT: Empties the field, restores the placeholder and
        # hides the password again.
        self._show_placeholder()
        self.hidden = True
        self._draw_eye()
