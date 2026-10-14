# Borrowise Application Starting Point
import tkinter as tk
from tkinter import ttk, messagebox


class BorrowiseApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Borrowise")

        
        # > THE WINDOW SETTINGS <
        

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+0+0"
        )

        self.root.resizable(False, False)

        try:
            self.root.state("zoomed")
        except:
            pass

        # > THE ACCOUNT'S DATABASE < ( BUT A TEMPORARY DICTIONARY)
        

        # This is the Format: "username": {"password": "...", "name": "..."}
        self.users = {
            "admin": {
                "password": "borrowise123",
                "name": "Administrator"
            }
        }

        
        # > A TEMPORARY RECORDS 
        

        self.records = []

        
        # > THE COLORS <
        
        self.bg_color = "#F5FAFF"

        self.dark_blue = "#123F87"
        self.blue = "#1677E8"
        self.medium_blue = "#4B96E8"

        self.light_blue = "#9CCCF5"
        self.lighter_blue = "#E8F4FF"

        self.border_blue = "#C8DDF2"
        self.text_gray = "#60799B"
        self.text_blue = "#123F87"

        self.sidebar_color = "#063B73"
        self.green = "#27B96F"
        self.purple = "#7655E8"
        self.orange = "#F5A623"

        self.white = "#FFFFFF"
        self.line_color = "#B9DDF5"

        
        # THE TKINTER STYLES BASE

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Borrowise.TCombobox",
            font=("Arial", 13),
            padding=8
        )

        style.configure(
            "Borrowise.Treeview",
            font=("Arial", 12),
            rowheight=35
        )

        style.configure(
            "Borrowise.Treeview.Heading",
            font=("Arial", 12, "bold")
        )

        
        # > THIS IS WHERE THE LOG IN SHOWS UP <
        

        self.show_login()

    
    # > THE MAIN LOGIN SCREEN <
    

    def show_login(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.background = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            bg=self.bg_color,
            highlightthickness=0
        )

        self.background.place(
            x=0,
            y=0
        )

        self.center_x = self.screen_width // 2

        self.create_logo()
        self.create_login_form()

    # ======================================================
    # BORROWISE LOGO
    # ======================================================

    def create_logo(self):

        cx = self.center_x
        cy = 145

        # Cube top
        self.background.create_polygon(
            cx, cy - 40,
            cx + 45, cy - 15,
            cx, cy + 12,
            cx - 45, cy - 15,
            fill="#F5FAFF",
            outline="#1555A5",
            width=3
        )

        # Cube left
        self.background.create_polygon(
            cx - 45, cy - 15,
            cx, cy + 12,
            cx, cy + 62,
            cx - 45, cy + 35,
            fill="#BFE1FA",
            outline="#1555A5",
            width=3
        )

        # Cube right
        self.background.create_polygon(
            cx, cy + 12,
            cx + 45, cy - 15,
            cx + 45, cy + 35,
            cx, cy + 62,
            fill="#8CC9F1",
            outline="#1555A5",
            width=3
        )

        # Title
        self.background.create_text(
            self.center_x,
            245,
            text="Borrowise",
            font=("Arial", 38, "bold"),
            fill="#0E3B82"
        )

        # Tagline
        self.background.create_text(
            self.center_x,
            282,
            text="Borrow • Track • Return",
            font=("Arial", 15, "bold"),
            fill="#5A78A0"
        )

    # ======================================================
    # LOGIN FORM
    # ======================================================

    def create_login_form(self):

        # Username
        self.username_frame = tk.Frame(
            self.root,
            bg="#FFFFFF",
            highlightbackground=self.border_blue,
            highlightthickness=2
        )

        self.username_frame.place(
            x=self.center_x,
            y=350,
            width=420,
            height=58,
            anchor="center"
        )

        self.create_user_icon(self.username_frame, 35, 29)

        self.username_entry = tk.Entry(
            self.username_frame,
            font=("Arial", 14),
            fg=self.text_gray,
            bg="#FFFFFF",
            bd=0,
            relief="flat"
        )

        self.username_entry.place(x=70, y=15, width=320, height=28)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", self.clear_username)

        # Password
        self.password_frame = tk.Frame(
            self.root,
            bg="#FFFFFF",
            highlightbackground=self.border_blue,
            highlightthickness=2
        )

        self.password_frame.place(
            x=self.center_x,
            y=420,
            width=420,
            height=58,
            anchor="center"
        )

        self.create_lock_icon(self.password_frame, 35, 29)

        self.password_entry = tk.Entry(
            self.password_frame,
            font=("Arial", 14),
            fg=self.text_gray,
            bg="#FFFFFF",
            bd=0,
            relief="flat"
        )

        self.password_entry.place(x=70, y=15, width=280, height=28)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.clear_password)

        self.password_visible = False

        self.eye_button = tk.Button(
            self.password_frame,
            text="👁",
            font=("Arial", 12),
            fg="#557AA7",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            activeforeground="#557AA7",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.toggle_password
        )

        self.eye_button.place(x=365, y=11, width=35, height=35)

        # Login Button
        self.login_button = tk.Button(
            self.root,
            text="LOGIN",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#1269D0",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.login
        )

        self.login_button.place(
            x=self.center_x,
            y=495,
            width=420,
            height=58,
            anchor="center"
        )

        self.root.bind("<Return>", lambda event: self.login())

        # Forgot Password
        self.forgot_password = tk.Button(
            self.root,
            text="Forgot password?",
            font=("Arial", 11, "bold"),
            fg="black",
            bg=self.bg_color,
            activeforeground="black",
            activebackground=self.bg_color,
            bd=0,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
            command=self.forgot_password_window
        )

        self.forgot_password.place(x=self.center_x, y=590, anchor="center")

        # Create Account
        self.create_account = tk.Button(
            self.root,
            text="Create new account",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#39FF14",
            activeforeground="white",
            activebackground="#32E612",
            bd=0,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
            padx=25,
            pady=8,
            command=self.create_account_window
        )

        self.create_account.place(x=self.center_x, y=635, anchor="center")

    # ======================================================
    # LOGIN FUNCTIONS
    # ======================================================

    def clear_username(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg="#123F87")

    def clear_password(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="#123F87")
            self.password_entry.config(show="•")

    def toggle_password(self):
        if not self.password_visible:
            self.password_entry.config(show="")
            self.password_visible = True
        else:
            if self.password_entry.get() != "Password":
                self.password_entry.config(show="•")
            self.password_visible = False

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "Username":
            username = ""
        if password == "Password":
            password = ""

        if (
            username in self.users
            and
            self.users[username]["password"] == password
        ):
            self.root.unbind("<Return>")
            self.show_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password."
            )

    # ======================================================
    # HELPER FOR FORM FIELD WITH EYE OPTION
    # ======================================================

    def build_form_field(self, parent, label_text, is_password=False):

        tk.Label(
            parent,
            text=label_text,
            font=("Arial", 11, "bold"),
            fg=self.text_blue,
            bg=self.bg_color
        ).pack(anchor="w", pady=(10, 3))

        field_frame = tk.Frame(
            parent,
            bg="#FFFFFF",
            highlightbackground=self.border_blue,
            highlightthickness=2
        )
        field_frame.pack(fill="x", ipady=4)

        entry = tk.Entry(
            field_frame,
            font=("Arial", 13),
            fg=self.text_blue,
            bg="#FFFFFF",
            bd=0,
            relief="flat"
        )

        if is_password:
            entry.config(show="•")
            entry.pack(side="left", fill="both", expand=True, padx=(12, 5), pady=6)

            state = {"visible": False}

            def toggle_eye():
                if not state["visible"]:
                    entry.config(show="")
                    state["visible"] = True
                else:
                    entry.config(show="•")
                    state["visible"] = False

            eye_btn = tk.Button(
                field_frame,
                text="👁",
                font=("Arial", 11),
                fg="#557AA7",
                bg="#FFFFFF",
                activebackground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                command=toggle_eye
            )
            eye_btn.pack(side="right", padx=(0, 10))
        else:
            entry.pack(fill="both", expand=True, padx=12, pady=6)

        return entry

    # ======================================================
    # CREATE ACCOUNT WINDOW (PERFECTLY ALIGNED GRID & UNIFORM SIZES)
    # ======================================================

    def create_account_window(self):

        win = tk.Toplevel(self.root)
        win.title("Create New Account")
        win.geometry("500x680")
        win.configure(bg=self.bg_color)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        # Center Window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 340
        win.geometry(f"+{x}+{y}")

        # Main Card Container
        card = tk.Frame(
            win,
            bg="#FFFFFF",
            padx=30,
            pady=25,
            relief="flat",
            highlightbackground=self.border_blue,
            highlightthickness=1.5
        )
        card.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        tk.Label(
            card,
            text="Create New Account",
            font=("Arial", 20, "bold"),
            fg=self.text_blue,
            bg="#FFFFFF"
        ).pack(pady=(0, 15))

        # Field Builder using GRID Layout for Perfect Alignment
        def create_field(label_text, is_pass=False):
            # Label
            lbl = tk.Label(
                card,
                text=label_text,
                font=("Arial", 11, "bold"),
                fg=self.text_blue,
                bg="#FFFFFF",
                anchor="w"
            )
            lbl.pack(fill="x", pady=(8, 3))

            # Entry Frame Box (Fixed Height & Border)
            entry_frame = tk.Frame(
                card,
                bg="#FFFFFF",
                height=38,
                highlightbackground=self.border_blue,
                highlightthickness=1.5
            )
            entry_frame.pack(fill="x")
            entry_frame.pack_propagate(False)

            # Grid Configuration inside frame
            entry_frame.columnconfigure(1, weight=1)

            icon_map = {
                "Full Name:": "👤",
                "Username:": "👤",
                "Password:": "🔒",
                "Confirm Password:": "🔒"
            }

            # Left Icon
            icon_lbl = tk.Label(
                entry_frame,
                text=icon_map.get(label_text, ""),
                fg=self.text_gray,
                bg="#FFFFFF",
                font=("Arial", 11)
            )
            icon_lbl.grid(row=0, column=0, padx=(10, 5), sticky="ns")

            # Entry Input Field
            entry = tk.Entry(
                entry_frame,
                font=("Arial", 12),
                bd=0,
                bg="#FFFFFF",
                fg=self.text_blue
            )
            entry.grid(row=0, column=1, sticky="nsew", pady=4)

            # Optional Eye Button for Password
            if is_pass:
                entry.config(show="•")
                state = {"visible": False}

                def toggle_eye():
                    if not state["visible"]:
                        entry.config(show="")
                        state["visible"] = True
                    else:
                        entry.config(show="•")
                        state["visible"] = False

                eye_btn = tk.Button(
                    entry_frame,
                    text="👁",
                    font=("Arial", 11),
                    fg="#557AA7",
                    bg="#FFFFFF",
                    activebackground="#FFFFFF",
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                    command=toggle_eye
                )
                eye_btn.grid(row=0, column=2, padx=(2, 10), sticky="ns")

            return entry

        # Input Fields
        self.name_entry = create_field("Full Name:")
        self.username_entry = create_field("Username:")
        self.password_entry = create_field("Password:", is_pass=True)
        self.confirm_entry = create_field("Confirm Password:", is_pass=True)

        # Registration Logic
        def create_account():
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm = self.confirm_entry.get().strip()

            if not name or not username or not password or not confirm:
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill out all fields.",
                    parent=win
                )
                return

            if username in self.users:
                messagebox.showerror(
                    "Error",
                    "Username already exists! Choose another.",
                    parent=win
                )
                return

            if password != confirm:
                messagebox.showerror(
                    "Error",
                    "Passwords do not match.",
                    parent=win
                )
                return

            # Save to Database
            self.users[username] = {
                "password": password,
                "name": name
            }

            win.destroy()

            # Automatic Direct Login to Dashboard & Success Message
            self.root.unbind("<Return>")
            self.show_dashboard()
            self.show_success_popup(message="Your account has been successfully created!")

        # Create Account Button
        btn = tk.Button(
            card,
            text="Create Account",
            font=("Arial", 12, "bold"),
            fg="#FFFFFF",
            bg=self.blue,
            activebackground="#1269D0",
            activeforeground="#FFFFFF",
            bd=0,
            pady=10,
            cursor="hand2",
            command=create_account
        )
        btn.pack(fill="x", pady=(22, 15))

        # Footer Link
        footer_frame = tk.Frame(card, bg="#FFFFFF")
        footer_frame.pack()

        lbl_footer = tk.Label(
            footer_frame,
            text="Already have an account? ",
            font=("Arial", 10),
            fg=self.text_gray,
            bg="#FFFFFF"
        )
        lbl_footer.pack(side="left")

        lbl_login = tk.Label(
            footer_frame,
            text="Log in",
            font=("Arial", 10, "bold"),
            fg=self.blue,
            bg="#FFFFFF",
            cursor="hand2"
        )
        lbl_login.pack(side="left")
        lbl_login.bind("<Button-1>", lambda event: win.destroy())

    # ======================================================
    # FORGOT PASSWORD WINDOW
    # ======================================================

    def forgot_password_window(self):

        win = tk.Toplevel(self.root)
        win.title("Forgot Password")
        win.geometry("520x420")
        win.configure(bg=self.bg_color)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        # Center Window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 260
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 210
        win.geometry(f"+{x}+{y}")

        tk.Label(
            win,
            text="Reset Password",
            font=("Arial", 22, "bold"),
            fg=self.dark_blue,
            bg=self.bg_color
        ).pack(pady=(25, 10))

        form_frame = tk.Frame(win, bg=self.bg_color, width=420)
        form_frame.pack(padx=50, fill="x")

        user_entry = self.build_form_field(form_frame, "Enter Username:")
        new_pass_entry = self.build_form_field(form_frame, "Enter New Password:", is_password=True)

        def reset_password():
            username = user_entry.get().strip()
            new_pass = new_pass_entry.get().strip()

            if not username or not new_pass:
                messagebox.showwarning("Input Error", "Please fill in all fields.", parent=win)
                return

            if username not in self.users:
                messagebox.showerror("Error", "Username not found!", parent=win)
                return

            self.users[username]["password"] = new_pass

            win.destroy()
            self.show_success_popup(message="Password updated successfully! You can now log in.")

        tk.Button(
            win,
            text="RESET PASSWORD",
            font=("Arial", 14, "bold"),
            fg="white",
            bg=self.blue,
            activebackground="#1269D0",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=reset_password
        ).pack(pady=30, ipadx=20, ipady=10)

    # ======================================================
    # USER ICON
    # ======================================================

    def create_user_icon(self, parent, x, y):
        canvas = tk.Canvas(parent, width=40, height=40, bg="white", highlightthickness=0)
        canvas.place(x=x - 20, y=y - 20)
        canvas.create_oval(14, 3, 26, 15, fill="#557AA7", outline="")
        canvas.create_oval(7, 17, 33, 37, fill="#557AA7", outline="")

    # ======================================================
    # LOCK ICON
    # ======================================================

    def create_lock_icon(self, parent, x, y):
        canvas = tk.Canvas(parent, width=40, height=40, bg="white", highlightthickness=0)
        canvas.place(x=x - 20, y=y - 20)
        lock_color = "#557AA7"
        canvas.create_arc(10, 4, 30, 24, start=0, extent=180, style="arc", outline=lock_color, width=4)
        canvas.create_line(10, 14, 10, 19, fill=lock_color, width=4)
        canvas.create_line(30, 14, 30, 19, fill=lock_color, width=4)
        canvas.create_rectangle(8, 17, 32, 36, fill=lock_color, outline="")
        canvas.create_oval(18, 21, 22, 25, fill="white", outline="")
        canvas.create_rectangle(19, 24, 21, 29, fill="white", outline="")

    # ======================================================
    # DASHBOARD
    # ======================================================

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_frame = tk.Frame(self.root, bg="#F2FAFF")
        self.main_frame.pack(fill="both", expand=True)

        self.create_sidebar()

        self.content_frame = tk.Frame(self.main_frame, bg="#F2FAFF")
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.dashboard_home()

    # ======================================================
    # SIDEBAR
    # ======================================================

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, bg="#063B73", width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_frame = tk.Frame(self.sidebar, bg="#063B73")
        logo_frame.pack(fill="x", padx=25, pady=(35, 30))

        tk.Label(
            logo_frame,
            text="📦",
            font=("Segoe UI Emoji", 38),
            fg="#CBEAFF",
            bg="#063B73"
        ).pack(side="left")

        logo_text = tk.Frame(logo_frame, bg="#063B73")
        logo_text.pack(side="left", padx=10)

        tk.Label(
            logo_text,
            text="Borrowise",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#063B73"
        ).pack(anchor="w")

        tk.Label(
            logo_text,
            text="Borrow • Track • Return",
            font=("Arial", 10),
            fg="#B9DDF5",
            bg="#063B73"
        ).pack(anchor="w", pady=(2, 0))

        self.create_sidebar_button(" 🏠", " Home", self.dashboard_home)
        self.create_sidebar_button(" ➕", "Borrow Item", self.show_borrow)
        self.create_sidebar_button(" 📦", "Return Item", self.show_return)
        self.create_sidebar_button(" 📋", " Records", self.show_records)
        self.create_sidebar_button(" 🔍", " Search", self.show_search)
        self.create_sidebar_button(" ↪", "Logout", self.logout)

    def create_sidebar_button(self, icon, text, command):
        button = tk.Button(
            self.sidebar,
            text=f" {icon} {text}",
            command=command,
            font=("Arial", 15),
            fg="white",
            bg="#063B73",
            activebackground="#168CF5",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=20,
            pady=15,
            cursor="hand2"
        )
        button.pack(fill="x", padx=20, pady=15)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def page_title(self, title, subtitle):
        tk.Label(
            self.content_frame,
            text=title,
            font=("Arial", 32, "bold"),
            fg="#123A8C",
            bg="#F2FAFF"
        ).pack(anchor="w", padx=45, pady=(40, 3))

        tk.Label(
            self.content_frame,
            text=subtitle,
            font=("Arial", 15),
            fg="#6689A8",
            bg="#F2FAFF"
        ).pack(anchor="w", padx=45, pady=(0, 25))

    def create_container(self, parent):
        container = tk.Frame(
            parent,
            bg="#F8FCFF",
            highlightbackground="#B9DDF5",
            highlightcolor="#B9DDF5",
            highlightthickness=2
        )
        return container

    # ======================================================
    # DASHBOARD HOME
    # ======================================================

    def dashboard_home(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Welcome to Borrowise!",
            font=("Arial", 36, "bold"),
            fg="#123A8C",
            bg="#F2FAFF"
        ).pack(anchor="w", padx=45, pady=(40, 3))

        tk.Label(
            self.content_frame,
            text="Easily manage and monitor your borrowed items.",
            font=("Arial", 16),
            fg="#6689A8",
            bg="#F2FAFF"
        ).pack(anchor="w", padx=45, pady=(0, 28))

        cards_frame = tk.Frame(self.content_frame, bg="#F2FAFF")
        cards_frame.pack(fill="x", padx=45)

        self.create_dashboard_card(cards_frame, "➕", "Borrow\nItem", "#168CF5", self.show_borrow).pack(side="left", fill="both", expand=True)
        self.create_dashboard_card(cards_frame, "📦", "Return\nItem", "#27B96F", self.show_return).pack(side="left", fill="both", expand=True, padx=8)
        self.create_dashboard_card(cards_frame, "📋", "View\nRecords", "#7655E8", self.show_records).pack(side="left", fill="both", expand=True, padx=8)
        self.create_dashboard_card(cards_frame, "🔍", " Search\nRecords", "#F5A623", self.show_search).pack(side="left", fill="both", expand=True)

        quote_container = tk.Frame(
            self.content_frame,
            bg="#E8F6FD",
            highlightbackground="#B9DDF5",
            highlightthickness=2
        )
        quote_container.pack(fill="x", padx=45, pady=40, ipady=22)

        tk.Label(quote_container, text="📦", font=("Segoe UI Emoji", 38), bg="#E8F6FD").pack(side="left", padx=(35, 20))

        quote_text = tk.Frame(quote_container, bg="#E8F6FD")
        quote_text.pack(side="left")

        tk.Label(quote_text, text="“Borrowise smart. Keep track.”", font=("Arial", 19, "bold"), fg="#123A8C", bg="#E8F6FD").pack(anchor="w")
        tk.Label(quote_text, text="— Borrowise", font=("Arial", 13), fg="#6689A8", bg="#E8F6FD").pack(anchor="w", pady=(4, 0))

    def create_dashboard_card(self, parent, icon, text, color, command):
        card = tk.Frame(parent, bg=color, height=205, cursor="hand2")
        card.pack_propagate(False)

        icon_label = tk.Label(card, text=icon, font=("Segoe UI Emoji", 40), fg="white", bg=color)
        icon_label.pack(pady=28)

        text_label = tk.Label(card, text=text, font=("Arial", 18, "bold"), fg="white", bg=color, justify="center")
        text_label.pack()

        card.bind("<Button-1>", lambda event: command())
        icon_label.bind("<Button-1>", lambda event: command())
        text_label.bind("<Button-1>", lambda event: command())

        return card

    # ======================================================
    # BORROW ITEM
    # ======================================================

    def show_borrow(self):
        self.clear_content()

        self.page_title("Borrow Item", "Enter the details of the item to be borrowed.")

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        form = tk.Frame(container, bg="#F8FCFF")
        form.pack(fill="x", padx=25, pady=25)

        self.borrower_entry = self.create_entry_row(form, "Borrower Name:", "Enter name")
        self.item_combo = self.create_combo_row(
            form,
            "Item Selection:",
            [
                "Select item", "Laptop", "Projector", "Keyboard",
                "Mouse", "Calculator", "Monitor", "Extension Cord", "Speaker"
            ]
        )
        self.quantity_spin = self.create_spinbox_row(form, "Quantity:")
        self.borrow_date_entry = self.create_entry_row(form, "Borrowing Date:", "MM-DD-YYYY")
        self.expected_return_entry = self.create_entry_row(form, "Expected Return Date:", "MM-DD-YYYY")
        self.status_combo = self.create_combo_row(form, "Status:", ["Borrowed", "Returned"])

        button_frame = tk.Frame(form, bg="#F8FCFF")
        button_frame.pack(pady=(18, 5))

        tk.Button(
            button_frame, text="Save / Borrow", font=("Arial", 15, "bold"), fg="white", bg=self.blue,
            activebackground="#087DDC", relief="flat", bd=0, padx=45, pady=12, cursor="hand2", command=self.borrow_item
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame, text="Clear", font=("Arial", 15, "bold"), fg=self.text_blue, bg="#DCEFFC",
            activebackground="#CBE9FA", relief="flat", bd=0, padx=45, pady=12, cursor="hand2", command=self.clear_borrow_form
        ).pack(side="left", padx=8)

    def create_entry_row(self, parent, label_text, placeholder):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row, text=label_text, font=("Arial", 14, "bold"), fg=self.text_blue, bg="#F8FCFF", width=22, anchor="w"
        ).pack(side="left")

        entry_container = tk.Frame(row, bg="white", highlightbackground=self.line_color, highlightcolor=self.line_color, highlightthickness=2)
        entry_container.pack(side="left", fill="x", expand=True)

        entry = tk.Entry(entry_container, font=("Arial", 13), fg="#47789E", bg="white", relief="flat", bd=0)
        entry.pack(fill="x", padx=10, pady=10)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.clear_placeholder(e, p))

        return entry

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.text_blue)

    def create_combo_row(self, parent, label_text, values):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row, text=label_text, font=("Arial", 14, "bold"), fg=self.text_blue, bg="#F8FCFF", width=22, anchor="w"
        ).pack(side="left")

        combo_container = tk.Frame(row, bg="white", highlightbackground=self.line_color, highlightcolor=self.line_color, highlightthickness=2)
        combo_container.pack(side="left", fill="x", expand=True)

        combo = ttk.Combobox(combo_container, values=values, state="readonly", style="Borrowise.TCombobox")
        combo.pack(fill="x", padx=2, pady=2)
        combo.current(0)

        return combo

    def create_spinbox_row(self, parent, label_text):
        row = tk.Frame(parent, bg="#F8FCFF")
        row.pack(fill="x", pady=7)

        tk.Label(
            row, text=label_text, font=("Arial", 14, "bold"), fg=self.text_blue, bg="#F8FCFF", width=22, anchor="w"
        ).pack(side="left")

        spin_container = tk.Frame(row, bg="white", highlightbackground=self.line_color, highlightthickness=2)
        spin_container.pack(side="left", fill="x", expand=True)

        spinbox = tk.Spinbox(spin_container, from_=1, to=100, font=("Arial", 13), relief="flat", bd=0, bg="white", fg=self.text_blue)
        spinbox.pack(fill="x", padx=10, pady=8)

        return spinbox

    def borrow_item(self):
        name = self.borrower_entry.get().strip()
        item = self.item_combo.get()
        quantity = self.quantity_spin.get().strip()
        borrow_date = self.borrow_date_entry.get().strip()
        return_date = self.expected_return_entry.get().strip()
        status = self.status_combo.get()

        if name == "" or name == "Enter name":
            messagebox.showwarning("Borrowise", "Please enter the borrower name.")
            return

        if item == "Select item":
            messagebox.showwarning("Borrowise", "Please select an item.")
            return

        if borrow_date == "" or borrow_date == "MM-DD-YYYY":
            messagebox.showwarning("Borrowise", "Please enter the borrowing date.")
            return

        if return_date == "" or return_date == "MM-DD-YYYY":
            messagebox.showwarning("Borrowise", "Please enter the expected return date.")
            return

        record = {
            "name": name,
            "item": item,
            "quantity": quantity,
            "borrow_date": borrow_date,
            "return_date": return_date,
            "status": status
        }

        self.records.append(record)
        self.show_success_popup(message="Item has been borrowed successfully.")

    def clear_borrow_form(self):
        self.borrower_entry.delete(0, tk.END)
        self.borrower_entry.insert(0, "Enter name")
        self.borrower_entry.config(fg="#47789E")

        self.item_combo.current(0)

        self.quantity_spin.delete(0, tk.END)
        self.quantity_spin.insert(0, "1")

        self.borrow_date_entry.delete(0, tk.END)
        self.borrow_date_entry.insert(0, "MM-DD-YYYY")
        self.borrow_date_entry.config(fg="#47789E")

        self.expected_return_entry.delete(0, tk.END)
        self.expected_return_entry.insert(0, "MM-DD-YYYY")
        self.expected_return_entry.config(fg="#47789E")

        self.status_combo.current(0)

    # ======================================================
    # CUSTOM DYNAMIC SUCCESS POPUP
    # ======================================================

    def show_success_popup(self, message="Item has been borrowed successfully."):

        popup = tk.Toplevel(self.root)
        popup.title("Borrowise")
        popup.geometry("450x230")
        popup.resizable(False, False)
        popup.configure(bg="#E3F0FC")
        popup.transient(self.root)
        popup.grab_set()

        # Center Popup Screen
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 225
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 115
        popup.geometry(f"450x230+{x}+{y}")

        # White Main Box
        main_card = tk.Frame(popup, bg="#FFFFFF")
        main_card.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Content Layout
        content_frame = tk.Frame(main_card, bg="#FFFFFF")
        content_frame.pack(expand=True, pady=(25, 10))

        # Green Circle Check Icon Canvas
        icon_canvas = tk.Canvas(
            content_frame,
            width=60,
            height=60,
            bg="#FFFFFF",
            highlightthickness=0
        )
        icon_canvas.pack(side="left", padx=(15, 20))

        # Draw Green Circle
        icon_canvas.create_oval(2, 2, 58, 58, fill="#28C76F", outline="")
        # Draw Checkmark Line
        icon_canvas.create_line(18, 30, 27, 39, fill="white", width=5, capstyle="round")
        icon_canvas.create_line(27, 39, 43, 21, fill="white", width=5, capstyle="round")

        # Text Layout
        text_frame = tk.Frame(content_frame, bg="#FFFFFF")
        text_frame.pack(side="left")

        tk.Label(
            text_frame,
            text="Success!",
            font=("Arial", 20, "bold"),
            fg="#0E3B82",
            bg="#FFFFFF"
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=message,
            font=("Arial", 11),
            fg="#5A78A0",
            bg="#FFFFFF",
            wraplength=260,
            justify="left"
        ).pack(anchor="w", pady=(3, 0))

        # OK Button (Centered Blue Button)
        btn_frame = tk.Frame(main_card, bg="#FFFFFF")
        btn_frame.pack(fill="x", pady=(0, 20))

        tk.Button(
            btn_frame,
            text="OK",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#1677E8",
            activebackground="#1269D0",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            width=16,
            pady=6,
            command=popup.destroy
        ).pack(anchor="center")

    
    # > THIS IS WHERE THE RETURN ITEM FUNCTIONALITY IS IMPLEMENTED <
    

    def show_return(self):

        self.clear_content()

        self.page_title("📦 Return Item", "Enter the details of the borrowed item.")

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        form = tk.Frame(container, bg="#F8FCFF")
        form.pack(fill="x", padx=25, pady=25)

        self.return_name_entry = self.create_entry_row(form, "Borrower Name:", "Enter name")
        self.return_item_entry = self.create_entry_row(form, "Item:", "Enter item")
        self.return_date_entry = self.create_entry_row(form, "Return Date:", "MM-DD-YYYY")

        tk.Button(
            form,
            text="📦 Mark as Returned",
            font=("Arial", 15, "bold"),
            fg="white",
            bg=self.green,
            activebackground="#1FA762",
            relief="flat",
            bd=0,
            padx=45,
            pady=12,
            cursor="hand2",
            command=self.return_item
        ).pack(pady=20)

        info_frame = tk.Frame(form, bg="#E8F6FD")
        info_frame.pack(fill="x", pady=(5, 5), padx=5)

        tk.Label(info_frame, text="ⓘ", font=("Arial", 20, "bold"), fg=self.blue, bg="#E8F6FD").pack(side="left", padx=(15, 10), pady=12)
        tk.Label(
            info_frame,
            text='The item status will be updated to\n"Returned" and the return date will be saved.',
            font=("Arial", 11),
            fg=self.text_blue,
            bg="#E8F6FD",
            justify="left"
        ).pack(side="left", pady=12)

    def return_item(self):
        name = self.return_name_entry.get().strip()
        item = self.return_item_entry.get().strip()
        return_date = self.return_date_entry.get().strip()

        if name == "" or name == "Enter name":
            messagebox.showwarning("Borrowise", "Please enter the borrower name.")
            return

        if item == "" or item == "Enter item":
            messagebox.showwarning("Borrowise", "Please enter the item.")
            return

        if return_date == "" or return_date == "MM-DD-YYYY":
            messagebox.showwarning("Borrowise", "Please enter the return date.")
            return

        found = False
        for record in self.records:
            if (
                record["name"].lower() == name.lower()
                and
                record["item"].lower() == item.lower()
                and
                record["status"] == "Borrowed"
            ):
                record["status"] = "Returned"
                record["return_date"] = return_date
                found = True
                break

        if found:
            self.show_success_popup(message="Item has been returned successfully.")
            self.show_records()
        else:
            messagebox.showwarning("Borrowise", "No matching borrowed item was found.")

    
    # > THIS IS THE BORROWING RECORDS FUNCTIONALITY IMPLEMENTED <
    

    def show_records(self):
        self.clear_content()

        self.page_title("Borrowing Records", "View all borrowed and returned items.")

        container = self.create_container(self.content_frame)
        container.pack(fill="x", padx=45, pady=5)

        table_frame = tk.Frame(container, bg="#F8FCFF")
        table_frame.pack(fill="x", padx=15, pady=15)

        columns = ("Name", "Item", "Quantity", "Borrow Date", "Return Date", "Status")

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
            style="Borrowise.Treeview"
        )

        for column in columns:
            table.heading(column, text=column)
            table.column(column, anchor="center", width=150)

        table.pack(fill="x")

        for record in self.records:
            table.insert(
                "",
                "end",
                values=(
                    record["name"],
                    record["item"],
                    record["quantity"],
                    record["borrow_date"],
                    record["return_date"],
                    record["status"]
                )
            )

        if len(self.records) == 0:
            tk.Label(
                container,
                text="No borrowing records available yet.",
                font=("Arial", 12),
                fg=self.text_gray,
                bg="#F8FCFF"
            ).pack(pady=(0, 15))

    # ======================================================
    # SEARCH RECORDS
    # ======================================================

    def show_search(self):
        self.clear_content()

        self.page_title("Search Records", "Search for borrowed or returned items.")

        search_container = self.create_container(self.content_frame)
        search_container.pack(fill="x", padx=45, pady=5)

        search_frame = tk.Frame(search_container, bg="#F8FCFF")
        search_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(search_frame, text="Search by:", font=("Arial", 13, "bold"), fg=self.text_blue, bg="#F8FCFF").pack(side="left", padx=5)

        self.search_combo = ttk.Combobox(
            search_frame,
            values=["Name", "Item", "Status", "Borrow Date", "Return Date"],
            state="readonly",
            style="Borrowise.TCombobox",
            width=15
        )
        self.search_combo.current(0)
        self.search_combo.pack(side="left", padx=5)

        search_input_container = tk.Frame(
            search_frame, bg="white", highlightbackground=self.line_color, highlightcolor=self.line_color, highlightthickness=2
        )
        search_input_container.pack(side="left", fill="x", expand=True, padx=5)

        self.search_entry = tk.Entry(search_input_container, font=("Arial", 13), relief="flat", bd=0, fg=self.text_blue)
        self.search_entry.pack(fill="x", padx=10, pady=9)
        self.search_entry.insert(0, "Enter keyword...")
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)

        tk.Button(
            search_frame, text="⌕ Search", font=("Arial", 13, "bold"), fg="white", bg=self.blue,
            activebackground="#087DDC", relief="flat", bd=0, padx=25, pady=10, cursor="hand2", command=self.search_records
        ).pack(side="left", padx=5)

        self.search_results_container = self.create_container(self.content_frame)
        self.search_results_container.pack(fill="x", padx=45, pady=20)

        results_frame = tk.Frame(self.search_results_container, bg="#F8FCFF")
        results_frame.pack(fill="x", padx=15, pady=15)

        columns = ("Name", "Item", "Quantity", "Borrow Date", "Return Date", "Status")

        self.search_table = ttk.Treeview(
            results_frame, columns=columns, show="headings", height=8, style="Borrowise.Treeview"
        )

        for column in columns:
            self.search_table.heading(column, text=column)
            self.search_table.column(column, anchor="center", width=150)

        self.search_table.pack(fill="x")

    def clear_search_placeholder(self, event):
        if self.search_entry.get() == "Enter keyword...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=self.text_blue)

    def search_records(self):
        keyword = self.search_entry.get().strip().lower()
        search_type = self.search_combo.get()

        for item in self.search_table.get_children():
            self.search_table.delete(item)

        if keyword == "" or keyword == "enter keyword...":
            return

        for record in self.records:
            if search_type == "Name":
                value = record["name"]
            elif search_type == "Item":
                value = record["item"]
            elif search_type == "Status":
                value = record["status"]
            elif search_type == "Borrow Date":
                value = record["borrow_date"]
            elif search_type == "Return Date":
                value = record["return_date"]
            else:
                value = ""

            if keyword in value.lower():
                self.search_table.insert(
                    "",
                    "end",
                    values=(
                        record["name"],
                        record["item"],
                        record["quantity"],
                        record["borrow_date"],
                        record["return_date"],
                        record["status"]
                    )
                )

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if answer:
            self.show_login()


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BorrowiseApp(root)

    root.mainloop()