import tkinter as tk
from tkinter import ttk
from controllers.auth_controller import AuthController
from utils.logger import Logger


class LoginView(ttk.Frame):
    def __init__(self, parent, login_callback, register_callback):
        super().__init__(parent)
        self.parent = parent
        self.login_callback = login_callback
        self.register_callback = register_callback
        self.auth_controller = AuthController()
        self.logger = Logger()

        # Configure grid layout
        self.pack(fill=tk.BOTH, expand=True)

        # Create main container with some padding
        self.main_container = ttk.Frame(self)
        self.main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create login frame with card style
        self.login_frame = ttk.Frame(self.main_container, style="Card.TFrame", padding=20)
        self.login_frame.pack(padx=20, pady=20)

        # Add logo or app name
        self.logo_label = ttk.Label(
            self.login_frame,
            text="Budget Manager",
            style="Title.TLabel"
        )
        self.logo_label.pack(pady=(10, 5))

        # Add welcome message
        self.welcome_label = ttk.Label(
            self.login_frame,
            text="Welcome back! Please login to your account.",
            style="Body.TLabel"
        )
        self.welcome_label.pack(pady=(0, 20))

        # Add username/password requirements
        self.requirements_label = ttk.Label(
            self.login_frame,
            text="Username: at least 3 characters | Password: at least 6 characters",
            style="Small.TLabel",
            foreground="#555555"
        )
        self.requirements_label.pack(pady=(0, 10))

        # Username label and entry
        self.username_label = ttk.Label(
            self.login_frame,
            text="Username",
            style="Body.TLabel"
        )
        self.username_label.pack(anchor=tk.W, padx=10)

        self.username_entry = ttk.Entry(
            self.login_frame,
            width=40,
            style="TEntry"
        )
        self.username_entry.pack(pady=(5, 15), padx=10, fill=tk.X)

        # Password label and entry
        self.password_label = ttk.Label(
            self.login_frame,
            text="Password",
            style="Body.TLabel"
        )
        self.password_label.pack(anchor=tk.W, padx=10)

        self.password_entry = ttk.Entry(
            self.login_frame,
            show="•",
            width=40,
            style="TEntry"
        )
        self.password_entry.pack(pady=(5, 15), padx=10, fill=tk.X)

        # Error message label
        self.error_label = ttk.Label(
            self.login_frame,
            text="",
            foreground="red",
            style="Small.TLabel"
        )
        self.error_label.pack(pady=(0, 15))

        # Login button - using tk.Button instead of ttk.Button for better styling
        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            command=self.login,
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.login_button.pack(pady=(5, 15))

        # Register link - using tk.Button instead of ttk.Button
        self.register_link = tk.Button(
            self.login_frame,
            text="Don't have an account? Register here",
            command=self.register_callback,
            bg="#f5f5f5",
            fg="#4a6da7",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0
        )
        self.register_link.pack(pady=(0, 10))

        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not username or not password:
            self.error_label.config(text="Please enter both username and password")
            return

        # Check username length
        if len(username) < 3:
            self.error_label.config(text="Username must be at least 3 characters")
            return

        # Check password length
        if len(password) < 6:
            self.error_label.config(text="Password must be at least 6 characters")
            return

        try:
            user = self.auth_controller.login(username, password)
            if user:
                self.login_callback(user)
            else:
                self.error_label.config(text="Invalid username or password")
        except Exception as e:
            self.logger.log_error(f"Login error: {str(e)}")
            self.error_label.config(text="An error occurred. Please try again.")

    def destroy(self):
        # Destroy all child widgets first
        for widget in self.winfo_children():
            widget.destroy()

        # Call parent destroy method
        self.pack_forget()
        ttk.Frame.destroy(self)
