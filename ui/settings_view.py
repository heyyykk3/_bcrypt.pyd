import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sv_ttk  # Add this import
from utils.logger import Logger
from utils.theme_manager import ThemeManager
import csv


class SettingsView(ttk.Frame):
    def __init__(self, parent, user, show_dashboard, theme_manager, db):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.show_dashboard = show_dashboard
        self.theme_manager = theme_manager
        self.db = db
        self.logger = Logger()

        # Add this line to initialize the transaction controller
        from controllers.transaction_controller import TransactionController
        self.transaction_controller = TransactionController()

        # Configure layout
        self.pack(fill=tk.BOTH, expand=True)

        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create sidebar and content frames
        self.sidebar_frame = ttk.Frame(self.main_container, style="Sidebar.TFrame", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create sidebar
        self.create_sidebar()

        # Create main content area
        self.create_main_content()

    def create_sidebar(self):
        # App logo/name
        self.logo_label = ttk.Label(
            self.sidebar_frame,
            text="Budget Manager",
            style="Heading.TLabel"
        )
        self.logo_label.pack(pady=(20, 10), padx=20)

        # User info
        self.user_frame = ttk.Frame(self.sidebar_frame)
        self.user_frame.pack(pady=(10, 20), padx=20, fill=tk.X)

        self.user_label = ttk.Label(
            self.user_frame,
            text=f"Welcome, {self.user.username}",
            style="Body.TLabel"
        )
        self.user_label.pack(side=tk.LEFT)

        # Navigation buttons
        self.dashboard_button = tk.Button(
            self.sidebar_frame,
            text="Dashboard",
            command=self.show_dashboard,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.dashboard_button.pack(pady=5, padx=20)

        self.settings_button = tk.Button(
            self.sidebar_frame,
            text="Settings",
            command=lambda: None,  # Already on settings
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.settings_button.pack(pady=5, padx=20)

    def create_main_content(self):
        # Header
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.pack(fill=tk.X, padx=20, pady=20)

        self.header_label = ttk.Label(
            self.header_frame,
            text="Settings",
            style="Title.TLabel"
        )
        self.header_label.pack(side=tk.LEFT)

        # Create a canvas with scrollbar for the content
        self.canvas = tk.Canvas(self.content_frame)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        self.scrollbar.pack(side="right", fill="y")

        # Appearance settings
        self.appearance_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.appearance_frame.pack(fill=tk.X, pady=(0, 20))

        self.appearance_title = ttk.Label(
            self.appearance_frame,
            text="Appearance",
            style="Subtitle.TLabel"
        )
        self.appearance_title.pack(padx=20, pady=(15, 10), anchor=tk.W)

        # Theme mode
        self.theme_frame = ttk.Frame(self.appearance_frame)
        self.theme_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.theme_label = ttk.Label(
            self.theme_frame,
            text="Theme Mode:",
            style="Body.TLabel"
        )
        self.theme_label.pack(side=tk.LEFT)

        self.theme_var = tk.StringVar(value="Light")

        self.theme_combobox = ttk.Combobox(
            self.theme_frame,
            textvariable=self.theme_var,
            values=["Light", "Dark"],
            state="readonly",
            width=20
        )
        self.theme_combobox.pack(side=tk.LEFT, padx=(20, 0))
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme_mode)

        # Account settings
        self.account_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.account_frame.pack(fill=tk.X, pady=(0, 20))

        self.account_title = ttk.Label(
            self.account_frame,
            text="Account",
            style="Subtitle.TLabel"
        )
        self.account_title.pack(padx=20, pady=(15, 10), anchor=tk.W)

        # Change password
        self.password_button = tk.Button(
            self.account_frame,
            text="Change Password",
            command=self.show_change_password_dialog,
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.password_button.pack(padx=20, pady=(0, 15))

        # Data settings
        self.data_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.data_frame.pack(fill=tk.X)

        self.data_title = ttk.Label(
            self.data_frame,
            text="Data",
            style="Subtitle.TLabel"
        )
        self.data_title.pack(padx=20, pady=(15, 10), anchor=tk.W)

        # Export data
        self.export_button = tk.Button(
            self.data_frame,
            text="Export Transactions",
            command=self.export_data,
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.export_button.pack(padx=20, pady=(0, 15))

    def change_theme_mode(self, event):
        try:
            new_mode = self.theme_var.get()
            if new_mode == "Dark":
                sv_ttk.set_theme("dark")
            else:
                sv_ttk.set_theme("light")
            self.logger.log_info(f"Theme mode changed to {new_mode}")
        except Exception as e:
            self.logger.log_error(f"Error changing theme mode: {str(e)}")

    def show_change_password_dialog(self):
        # Create dialog
        dialog = tk.Toplevel(self)
        dialog.title("Change Password")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make dialog modal

        # Center dialog on parent window
        dialog.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - dialog.winfo_width()) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Dialog content
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            frame,
            text="Change Password",
            style="Subtitle.TLabel"
        )
        title_label.pack(pady=(0, 20))

        # Form fields
        # Current password
        current_label = ttk.Label(frame, text="Current Password:", style="Body.TLabel")
        current_label.pack(anchor=tk.W)

        current_entry = ttk.Entry(frame, show="•", width=40)
        current_entry.pack(pady=(5, 15), fill=tk.X)

        # New password
        new_label = ttk.Label(frame, text="New Password:", style="Body.TLabel")
        new_label.pack(anchor=tk.W)

        new_entry = ttk.Entry(frame, show="•", width=40)
        new_entry.pack(pady=(5, 15), fill=tk.X)

        # Confirm new password
        confirm_label = ttk.Label(frame, text="Confirm New Password:", style="Body.TLabel")
        confirm_label.pack(anchor=tk.W)

        confirm_entry = ttk.Entry(frame, show="•", width=40)
        confirm_entry.pack(pady=(5, 15), fill=tk.X)

        # Error message label
        error_label = ttk.Label(
            frame,
            text="",
            foreground="red",
            style="Small.TLabel"
        )
        error_label.pack(pady=(0, 15))

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)

        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            style="Secondary.TButton",
            width=15
        )
        cancel_button.pack(side=tk.LEFT, padx=(0, 10))

        def change_password():
            # Implementation for changing password
            pass

        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=change_password,
            style="Primary.TButton",
            width=15
        )
        save_button.pack(side=tk.LEFT)

    def export_data(self):
        try:
            # Ask for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Transactions"
            )

            if not file_path:
                return  # User cancelled

            # Get transactions
            transactions = self.transaction_controller.get_user_transactions(self.user.id)

            # Write to CSV
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(['Date', 'Description', 'Category', 'Amount'])

                # Write transactions
                for t in transactions:
                    writer.writerow([
                        t.date.strftime("%Y-%m-%d"),
                        t.description,
                        t.category,
                        t.amount
                    ])

            messagebox.showinfo("Export Successful", f"Transactions exported to {file_path}")
            self.logger.log_info(f"Transactions exported to {file_path}")

        except Exception as e:
            self.logger.log_error(f"Error exporting data: {str(e)}")
            messagebox.showerror("Export Failed", "An error occurred while exporting data.")

    def destroy(self):
        # Destroy all child widgets first
        for widget in self.winfo_children():
            widget.destroy()

        # Call parent destroy method
        self.pack_forget()
        ttk.Frame.destroy(self)
