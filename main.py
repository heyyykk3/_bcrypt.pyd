import tkinter as tk
from tkinter import ttk
import sv_ttk  # For modern theme
import os
import gc  # For garbage collection

from ui.login_view import LoginView
from ui.register_view import RegisterView
from ui.dashboard_view import DashboardView
from ui.transaction_view import TransactionView
from ui.category_view import CategoryView
from ui.settings_view import SettingsView
from database.db import Database
from utils.logger import Logger
from utils.theme_manager import ThemeManager


class BudgetManagerApp:
    def __init__(self):
        # Initialize logger
        self.logger = Logger()
        self.logger.log_info("Application starting...")

        # Check if database exists, if not, delete it to recreate with correct schema
        if os.path.exists("budget_manager.db"):
            try:
                # Try to connect and check schema
                import sqlite3
                conn = sqlite3.connect("budget_manager.db")
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(users)")
                columns = cursor.fetchall()
                column_names = [column[1] for column in columns]

                if 'email' not in column_names:
                    self.logger.log_info("Database schema outdated, recreating database...")
                    conn.close()
                    os.remove("budget_manager.db")
                conn.close()
            except Exception as e:
                self.logger.log_error(f"Error checking database schema: {str(e)}")

        # Initialize database
        self.db = Database()
        self.db.initialize()

        # Initialize theme manager
        self.theme_manager = ThemeManager()

        # Setup main window
        self.root = tk.Tk()
        self.root.title("Budget Manager")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        # Apply modern theme
        sv_ttk.set_theme("light")

        # Configure styles
        self.configure_styles()

        # Initialize views
        self.current_view = None
        self.current_user = None

        # Start with login view
        self.show_login()

        # Start the application
        self.root.mainloop()

    def configure_styles(self):
        """Configure ttk styles for the application"""
        style = ttk.Style()

        # Configure frame styles
        style.configure("Card.TFrame", background="#ffffff", relief="raised")
        style.configure("Sidebar.TFrame", background="#f0f0f0")

        # Configure label styles
        style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), padding=5)
        style.configure("Subtitle.TLabel", font=("Helvetica", 18, "bold"), padding=3)
        style.configure("Heading.TLabel", font=("Helvetica", 16, "bold"), padding=2)
        style.configure("Body.TLabel", font=("Helvetica", 12), padding=1)
        style.configure("Small.TLabel", font=("Helvetica", 10), padding=1)

        # Configure button styles
        style.configure("Primary.TButton", font=("Helvetica", 12), padding=5)
        style.configure("Secondary.TButton", font=("Helvetica", 12), padding=5)
        style.configure("Danger.TButton", font=("Helvetica", 12), padding=5)

        # Configure entry styles
        style.configure("TEntry", font=("Helvetica", 12), padding=5)

        # Configure separator style
        style.configure("TSeparator", background="#e0e0e0")

        # Add custom styles for cards with shadows
        style.configure("Card.TFrame", background="#ffffff", relief="raised", borderwidth=1)

        # Configure combobox style
        style.configure("TCombobox", padding=5, font=("Helvetica", 12))

        # Configure scrollbar style
        style.configure("TScrollbar", background="#f0f0f0", troughcolor="#e0e0e0",
                        borderwidth=0, arrowsize=13)

        # Configure progressbar style
        style.configure("TProgressbar", background="#4a6da7", troughcolor="#e0e0e0",
                        borderwidth=0, thickness=10)

    def show_login(self):
        self.clear_current_view()
        self.current_view = LoginView(self.root, self.login_callback, self.show_register)

    def show_register(self):
        self.clear_current_view()
        self.current_view = RegisterView(self.root, self.register_callback, self.show_login)

    def show_dashboard(self):
        self.clear_current_view()
        self.current_view = DashboardView(
            self.root,
            self.current_user,
            self.show_transactions,
            self.show_categories,
            self.show_settings,
            self.logout
        )

    def show_transactions(self):
        self.clear_current_view()
        self.current_view = TransactionView(
            self.root,
            self.current_user,
            self.show_dashboard,
            self.db
        )

    def show_categories(self):
        self.clear_current_view()
        self.current_view = CategoryView(
            self.root,
            self.current_user,
            self.show_dashboard,
            self.db
        )

    def show_settings(self):
        self.clear_current_view()
        self.current_view = SettingsView(
            self.root,
            self.current_user,
            self.show_dashboard,
            self.theme_manager,
            self.db
        )

    def clear_current_view(self):
        """Thoroughly clean up the current view to prevent duplication"""
        if self.current_view:
            try:
                # Call the view's destroy method which should handle proper cleanup
                self.current_view.destroy()

                # Set to None to ensure garbage collection
                self.current_view = None

                # Force garbage collection to clean up any lingering references
                gc.collect()

                # Update the root window to ensure all widgets are properly removed
                self.root.update()
            except Exception as e:
                self.logger.log_error(f"Error clearing view: {str(e)}")
                # Fallback method if the above fails
                try:
                    if hasattr(self.current_view, 'pack_forget'):
                        self.current_view.pack_forget()

                    # Destroy all children of the current view
                    for widget in self.current_view.winfo_children():
                        widget.destroy()

                    # Then destroy the view itself
                    self.current_view.destroy()
                except:
                    pass

                self.current_view = None
                gc.collect()
                self.root.update()

    def login_callback(self, user):
        self.current_user = user
        self.logger.log_info(f"User logged in: {user.username}")
        self.show_dashboard()

    def register_callback(self, user):
        self.current_user = user
        self.logger.log_info(f"New user registered: {user.username}")
        self.show_dashboard()

    def logout(self):
        self.current_user = None
        self.logger.log_info("User logged out")
        self.show_login()


if __name__ == "__main__":
    app = BudgetManagerApp()
