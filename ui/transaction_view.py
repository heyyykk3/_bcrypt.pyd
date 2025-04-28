import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.transaction_controller import TransactionController
from utils.logger import Logger


class TransactionView(ttk.Frame):
    def __init__(self, parent, user, show_dashboard, db):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.show_dashboard = show_dashboard
        self.db = db
        self.transaction_controller = TransactionController()
        self.logger = Logger()

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

        # Load transactions
        self.load_transactions()

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

        self.transactions_button = tk.Button(
            self.sidebar_frame,
            text="Transactions",
            command=lambda: None,  # Already on transactions
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.transactions_button.pack(pady=5, padx=20)

    def create_main_content(self):
        # Header
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.pack(fill=tk.X, padx=20, pady=20)

        self.header_label = ttk.Label(
            self.header_frame,
            text="Transactions",
            style="Title.TLabel"
        )
        self.header_label.pack(side=tk.LEFT)

        # Add transaction button
        self.add_button = tk.Button(
            self.header_frame,
            text="+ Add Transaction",
            command=self.show_add_transaction_dialog,
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=15,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.add_button.pack(side=tk.RIGHT)

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

        # Transactions table
        self.transactions_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.transactions_frame.pack(fill=tk.X, pady=(0, 20))

        # Table header
        self.table_header = ttk.Frame(self.transactions_frame)
        self.table_header.pack(fill=tk.X, padx=10, pady=10)

        headers = ["Date", "Description", "Category", "Amount", "Actions"]
        widths = [100, 200, 150, 100, 150]

        for i, (header, width) in enumerate(zip(headers, widths)):
            header_label = ttk.Label(
                self.table_header,
                text=header,
                style="Body.TLabel",
                font=("Helvetica", 12, "bold"),
                width=width
            )
            header_label.pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(self.transactions_frame, orient="horizontal").pack(fill=tk.X, padx=10)

        # Placeholder for transactions (will be populated in load_transactions)
        self.transactions_container = ttk.Frame(self.transactions_frame)
        self.transactions_container.pack(fill=tk.X, padx=10, pady=10)
        self.transaction_rows = []

    def load_transactions(self):
        try:
            # Clear existing transactions
            for row in self.transaction_rows:
                row.destroy()
            self.transaction_rows = []

            # Get user's transactions
            transactions = self.transaction_controller.get_user_transactions(self.user.id)

            if not transactions:
                # No transactions to show
                no_data_frame = ttk.Frame(self.transactions_container)
                no_data_frame.pack(fill=tk.X, pady=20)

                no_data_label = ttk.Label(
                    no_data_frame,
                    text="No transactions found. Add a new transaction to get started.",
                    style="Body.TLabel"
                )
                no_data_label.pack()

                self.transaction_rows.append(no_data_frame)
                return

            # Sort transactions by date (newest first)
            transactions.sort(key=lambda t: t.date, reverse=True)

            # Add transactions to table
            for transaction in transactions:
                row_frame = ttk.Frame(self.transactions_container)
                row_frame.pack(fill=tk.X, pady=5)

                # Date
                date_label = ttk.Label(
                    row_frame,
                    text=transaction.date.strftime("%m/%d/%Y"),
                    style="Body.TLabel",
                    width=100
                )
                date_label.pack(side=tk.LEFT, padx=5)

                # Description
                desc_label = ttk.Label(
                    row_frame,
                    text=transaction.description,
                    style="Body.TLabel",
                    width=200
                )
                desc_label.pack(side=tk.LEFT, padx=5)

                # Category
                category_label = ttk.Label(
                    row_frame,
                    text=transaction.category,
                    style="Body.TLabel",
                    width=150
                )
                category_label.pack(side=tk.LEFT, padx=5)

                # Amount (with color)
                amount_color = "#4caf50" if transaction.amount > 0 else "#ef5350"
                amount_text = f"+${transaction.amount:.2f}" if transaction.amount > 0 else f"-${abs(transaction.amount):.2f}"

                amount_label = ttk.Label(
                    row_frame,
                    text=amount_text,
                    foreground=amount_color,
                    style="Body.TLabel",
                    width=100
                )
                amount_label.pack(side=tk.LEFT, padx=5)

                # Actions
                actions_frame = ttk.Frame(row_frame)
                actions_frame.pack(side=tk.LEFT, padx=5)

                edit_button = tk.Button(
                    actions_frame,
                    text="Edit",
                    command=lambda t=transaction: self.show_edit_transaction_dialog(t),
                    bg="#f0f0f0",
                    fg="#333333",
                    font=("Helvetica", 10),
                    width=8,
                    relief=tk.RAISED,
                    cursor="hand2"
                )
                edit_button.pack(side=tk.LEFT, padx=(0, 5))

                delete_button = tk.Button(
                    actions_frame,
                    text="Delete",
                    command=lambda t=transaction: self.delete_transaction(t),
                    bg="#ef5350",
                    fg="white",
                    font=("Helvetica", 10),
                    width=8,
                    relief=tk.RAISED,
                    cursor="hand2"
                )
                delete_button.pack(side=tk.LEFT)

                self.transaction_rows.append(row_frame)

        except Exception as e:
            self.logger.log_error(f"Error loading transactions: {str(e)}")

    def show_add_transaction_dialog(self):
        # Create dialog
        dialog = tk.Toplevel(self)
        dialog.title("Add Transaction")
        dialog.geometry("400x450")
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
            text="Add New Transaction",
            style="Subtitle.TLabel"
        )
        title_label.pack(pady=(0, 20))

        # Form fields
        # Description
        desc_label = ttk.Label(frame, text="Description:", style="Body.TLabel")
        desc_label.pack(anchor=tk.W)

        desc_entry = ttk.Entry(frame, width=40, style="TEntry")
        desc_entry.pack(pady=(5, 15), fill=tk.X)

        # Amount
        amount_label = ttk.Label(frame, text="Amount:", style="Body.TLabel")
        amount_label.pack(anchor=tk.W)

        amount_frame = ttk.Frame(frame)
        amount_frame.pack(fill=tk.X, pady=(5, 0))

        # Radio buttons for income/expense
        transaction_type = tk.StringVar(value="expense")

        expense_radio = ttk.Radiobutton(
            amount_frame,
            text="Expense",
            variable=transaction_type,
            value="expense"
        )
        expense_radio.pack(side=tk.LEFT, padx=(0, 10))

        income_radio = ttk.Radiobutton(
            amount_frame,
            text="Income",
            variable=transaction_type,
            value="income"
        )
        income_radio.pack(side=tk.LEFT)

        amount_entry = ttk.Entry(frame, width=40, style="TEntry")
        amount_entry.pack(pady=(5, 15), fill=tk.X)

        # Category
        category_label = ttk.Label(frame, text="Category:", style="Body.TLabel")
        category_label.pack(anchor=tk.W)

        # Get categories from database
        categories = ["Food", "Transportation", "Housing", "Entertainment", "Utilities", "Healthcare", "Other"]

        category_var = tk.StringVar(value="Other")
        category_combobox = ttk.Combobox(frame, textvariable=category_var, values=categories, state="readonly",
                                         width=38)
        category_combobox.pack(pady=(5, 15), fill=tk.X)

        # Date
        date_label = ttk.Label(frame, text="Date:", style="Body.TLabel")
        date_label.pack(anchor=tk.W)

        date_frame = ttk.Frame(frame)
        date_frame.pack(fill=tk.X, pady=(5, 15))

        # Current date as default
        today = datetime.now()

        # Month, day, year entries
        month_var = tk.StringVar(value=str(today.month))
        month_entry = ttk.Entry(date_frame, textvariable=month_var, width=5)
        month_entry.pack(side=tk.LEFT, padx=(0, 5))

        month_label = ttk.Label(date_frame, text="/", style="Body.TLabel")
        month_label.pack(side=tk.LEFT, padx=(0, 5))

        day_var = tk.StringVar(value=str(today.day))
        day_entry = ttk.Entry(date_frame, textvariable=day_var, width=5)
        day_entry.pack(side=tk.LEFT, padx=(0, 5))

        day_label = ttk.Label(date_frame, text="/", style="Body.TLabel")
        day_label.pack(side=tk.LEFT, padx=(0, 5))

        year_var = tk.StringVar(value=str(today.year))
        year_entry = ttk.Entry(date_frame, textvariable=year_var, width=8)
        year_entry.pack(side=tk.LEFT)

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
        button_frame.pack(fill=tk.X, pady=(10, 0))

        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            style="Secondary.TButton",
            width=15
        )
        cancel_button.pack(side=tk.LEFT, padx=(0, 10))

        def save_transaction():
            try:
                # Validate inputs
                description = desc_entry.get().strip()
                if not description:
                    error_label.config(text="Please enter a description")
                    return

                # Parse amount
                try:
                    amount = float(amount_entry.get().strip())
                    if amount <= 0:
                        error_label.config(text="Amount must be greater than zero")
                        return

                    # Make amount negative for expenses
                    if transaction_type.get() == "expense":
                        amount = -amount
                except ValueError:
                    error_label.config(text="Please enter a valid amount")
                    return

                # Get category
                category = category_var.get()

                # Parse date
                try:
                    month = int(month_var.get().strip())
                    day = int(day_var.get().strip())
                    year = int(year_var.get().strip())

                    if not (1 <= month <= 12 and 1 <= day <= 31 and 1000 <= year <= 9999):
                        error_label.config(text="Please enter a valid date")
                        return

                    date = datetime(year, month, day)
                except ValueError:
                    error_label.config(text="Please enter a valid date")
                    return

                # Create transaction
                self.transaction_controller.add_transaction(
                    user_id=self.user.id,
                    description=description,
                    amount=amount,
                    category=category,
                    date=date
                )

                # Reload transactions
                self.load_transactions()

                # Close dialog
                dialog.destroy()

            except Exception as e:
                self.logger.log_error(f"Error adding transaction: {str(e)}")
                error_label.config(text="An error occurred. Please try again.")

        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=save_transaction,
            style="Primary.TButton",
            width=15
        )
        save_button.pack(side=tk.LEFT)

    def show_edit_transaction_dialog(self, transaction):
        # Implementation similar to show_add_transaction_dialog but pre-filled with transaction data
        pass

    def delete_transaction(self, transaction):
        # Confirm dialog
        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete this transaction?\n\n{transaction.description}"
        ):
            try:
                # Delete transaction
                self.transaction_controller.delete_transaction(transaction.id)

                # Reload transactions
                self.load_transactions()
            except Exception as e:
                self.logger.log_error(f"Error deleting transaction: {str(e)}")
                messagebox.showerror(
                    "Error",
                    "An error occurred while deleting the transaction. Please try again."
                )

    def destroy(self):
        # Destroy all child widgets first
        for widget in self.winfo_children():
            widget.destroy()

        # Clear references to widgets
        self.transaction_rows = []

        # Call parent destroy method
        self.pack_forget()
        ttk.Frame.destroy(self)
