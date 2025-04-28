import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
from controllers.transaction_controller import TransactionController
from utils.logger import Logger


class DashboardView(ttk.Frame):
    def __init__(self, parent, user, show_transactions, show_categories, show_settings, logout):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.show_transactions = show_transactions
        self.show_categories = show_categories
        self.show_settings = show_settings
        self.logout = logout
        self.transaction_controller = TransactionController()
        self.logger = Logger()

        # Store references to matplotlib figures for proper cleanup
        self.category_figure = None
        self.trend_figure = None

        # Store references to canvases
        self.category_canvas = None
        self.trend_canvas = None

        # Store references to widgets that need cleanup
        self.transaction_widgets = []

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

        # Load data
        self.load_data()

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
            command=lambda: None,  # Already on dashboard
            bg="#4a6da7",
            fg="white",
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
            command=self.show_transactions,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.transactions_button.pack(pady=5, padx=20)

        self.categories_button = tk.Button(
            self.sidebar_frame,
            text="Categories",
            command=self.show_categories,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.categories_button.pack(pady=5, padx=20)

        self.settings_button = tk.Button(
            self.sidebar_frame,
            text="Settings",
            command=self.show_settings,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.settings_button.pack(pady=5, padx=20)

        # Add a spacer
        ttk.Frame(self.sidebar_frame).pack(fill=tk.Y, expand=True)

        # Logout button at bottom
        self.logout_button = tk.Button(
            self.sidebar_frame,
            text="Logout",
            command=self.logout,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.logout_button.pack(pady=(5, 20), padx=20)

    def create_main_content(self):
        # Header
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.pack(fill=tk.X, padx=20, pady=20)

        self.header_label = ttk.Label(
            self.header_frame,
            text="Dashboard",
            style="Title.TLabel"
        )
        self.header_label.pack(side=tk.LEFT)

        self.date_label = ttk.Label(
            self.header_frame,
            text=datetime.now().strftime("%B %d, %Y"),
            style="Body.TLabel"
        )
        self.date_label.pack(side=tk.RIGHT)

        # Create a proper scrollable frame with fixed scrollbar
        self.outer_frame = ttk.Frame(self.content_frame)
        self.outer_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.outer_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Pack canvas and scrollbar properly
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create scrollable frame inside canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Enable mousewheel scrolling
        self.bind_mousewheel()

        # Summary cards row with improved spacing and sizing
        self.summary_frame = ttk.Frame(self.scrollable_frame)
        self.summary_frame.pack(fill=tk.X, pady=(0, 20))

        # Income card with improved styling
        self.income_card = ttk.Frame(self.summary_frame, style="Card.TFrame", padding=15)
        self.income_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        income_icon_label = ttk.Label(self.income_card, text="↑", font=("Helvetica", 18), foreground="#2e7d32")
        income_icon_label.pack(side=tk.LEFT, padx=(0, 10))

        income_text_frame = ttk.Frame(self.income_card)
        income_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.income_title = ttk.Label(
            income_text_frame,
            text="Income",
            style="Body.TLabel"
        )
        self.income_title.pack(anchor=tk.W)

        self.income_amount = ttk.Label(
            income_text_frame,
            text="$0.00",
            foreground="#2e7d32",  # Green color
            font=("Helvetica", 18, "bold")
        )
        self.income_amount.pack(anchor=tk.W)

        # Expenses card with improved styling
        self.expenses_card = ttk.Frame(self.summary_frame, style="Card.TFrame", padding=15)
        self.expenses_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        expenses_icon_label = ttk.Label(self.expenses_card, text="↓", font=("Helvetica", 18), foreground="#c62828")
        expenses_icon_label.pack(side=tk.LEFT, padx=(0, 10))

        expenses_text_frame = ttk.Frame(self.expenses_card)
        expenses_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.expenses_title = ttk.Label(
            expenses_text_frame,
            text="Expenses",
            style="Body.TLabel"
        )
        self.expenses_title.pack(anchor=tk.W)

        self.expenses_amount = ttk.Label(
            expenses_text_frame,
            text="$0.00",
            foreground="#c62828",  # Red color
            font=("Helvetica", 18, "bold")
        )
        self.expenses_amount.pack(anchor=tk.W)

        # Balance card with improved styling
        self.balance_card = ttk.Frame(self.summary_frame, style="Card.TFrame", padding=15)
        self.balance_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        balance_icon_label = ttk.Label(self.balance_card, text="=", font=("Helvetica", 18))
        balance_icon_label.pack(side=tk.LEFT, padx=(0, 10))

        balance_text_frame = ttk.Frame(self.balance_card)
        balance_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.balance_title = ttk.Label(
            balance_text_frame,
            text="Balance",
            style="Body.TLabel"
        )
        self.balance_title.pack(anchor=tk.W)

        self.balance_amount = ttk.Label(
            balance_text_frame,
            text="$0.00",
            font=("Helvetica", 18, "bold")
        )
        self.balance_amount.pack(anchor=tk.W)

        # Charts row with fixed heights
        self.charts_frame = ttk.Frame(self.scrollable_frame)
        self.charts_frame.pack(fill=tk.X, pady=(0, 20))

        # Expense by category chart with fixed height
        self.category_chart_frame = ttk.Frame(self.charts_frame, style="Card.TFrame")
        self.category_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.category_chart_title = ttk.Label(
            self.category_chart_frame,
            text="Expenses by Category",
            style="Subtitle.TLabel"
        )
        self.category_chart_title.pack(padx=20, pady=(15, 5), anchor=tk.W)

        self.category_chart_container = ttk.Frame(self.category_chart_frame, height=300)
        self.category_chart_container.pack(padx=20, pady=(0, 15), fill=tk.BOTH, expand=True)
        self.category_chart_container.pack_propagate(False)  # Prevent shrinking

        # Monthly trend chart with fixed height
        self.trend_chart_frame = ttk.Frame(self.charts_frame, style="Card.TFrame")
        self.trend_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.trend_chart_title = ttk.Label(
            self.trend_chart_frame,
            text="Monthly Trend",
            style="Subtitle.TLabel"
        )
        self.trend_chart_title.pack(padx=20, pady=(15, 5), anchor=tk.W)

        self.trend_chart_container = ttk.Frame(self.trend_chart_frame, height=300)
        self.trend_chart_container.pack(padx=20, pady=(0, 15), fill=tk.BOTH, expand=True)
        self.trend_chart_container.pack_propagate(False)  # Prevent shrinking

        # Recent transactions with improved styling
        self.transactions_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.transactions_frame.pack(fill=tk.X, pady=(0, 20))

        self.transactions_header = ttk.Frame(self.transactions_frame)
        self.transactions_header.pack(fill=tk.X, padx=20, pady=(15, 10))

        self.transactions_title = ttk.Label(
            self.transactions_header,
            text="Recent Transactions",
            style="Subtitle.TLabel"
        )
        self.transactions_title.pack(side=tk.LEFT)

        self.view_all_button = tk.Button(
            self.transactions_header,
            text="View All",
            command=self.show_transactions,
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 10),
            width=10,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.view_all_button.pack(side=tk.RIGHT)

        # Transactions list with fixed height
        self.transactions_list = ttk.Frame(self.transactions_frame)
        self.transactions_list.pack(fill=tk.X, padx=20, pady=(0, 15))

        # Update scrollregion after all widgets are added
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Update the scrollable frame width when canvas size changes
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        # Update the scrollregion to encompass all the content
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_mousewheel(self):
        # Bind mousewheel to canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def unbind_mousewheel(self):
        # Unbind mousewheel when view is destroyed
        try:
            self.canvas.unbind_all("<MouseWheel>")
        except:
            pass

    def _on_mousewheel(self, event):
        # Handle mousewheel scrolling
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def cleanup_matplotlib_figures(self):
        # Clean up matplotlib figures to prevent memory leaks
        if self.category_figure:
            plt.close(self.category_figure)
            self.category_figure = None

        if self.trend_figure:
            plt.close(self.trend_figure)
            self.trend_figure = None

    def load_data(self):
        try:
            # Clean up any existing matplotlib figures
            self.cleanup_matplotlib_figures()

            # Get user's transactions
            transactions = self.transaction_controller.get_user_transactions(self.user.id)

            # Calculate summary
            income = sum(t.amount for t in transactions if t.amount > 0)
            expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
            balance = income - expenses

            # Update summary cards
            self.income_amount.config(text=f"${income:.2f}")
            self.expenses_amount.config(text=f"${expenses:.2f}")
            self.balance_amount.config(text=f"${balance:.2f}")

            # Create category chart
            self.create_category_chart(transactions)

            # Create trend chart
            self.create_trend_chart(transactions)

            # Display recent transactions
            self.display_recent_transactions(transactions[:5])  # Show only 5 most recent

            # Update scrollregion after all data is loaded
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        except Exception as e:
            self.logger.log_error(f"Error loading dashboard data: {str(e)}")

    def create_category_chart(self, transactions):
        # Clear previous chart if exists
        for widget in self.category_chart_container.winfo_children():
            widget.destroy()

        # Clean up previous matplotlib figure if exists
        if self.category_figure:
            plt.close(self.category_figure)

        # Filter expenses only and group by category
        expenses = [t for t in transactions if t.amount < 0]
        if not expenses:
            # No expenses to show
            no_data_label = ttk.Label(
                self.category_chart_container,
                text="No expense data to display",
                style="Body.TLabel"
            )
            no_data_label.pack(pady=50)
            return

        # Group by category
        categories = {}
        for t in expenses:
            if t.category in categories:
                categories[t.category] += abs(t.amount)
            else:
                categories[t.category] = abs(t.amount)

        # Create pie chart with improved styling
        self.category_figure, ax = plt.subplots(figsize=(4, 3), dpi=100, facecolor='#f8f9fa')

        # Custom colors for better visual appeal
        colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#1a535c', '#f7b801',
                  '#7bdff2', '#b2f7ef', '#f7d6e0', '#2ec4b6', '#e71d36']

        wedges, texts, autotexts = ax.pie(
            categories.values(),
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            colors=colors[:len(categories)],
            wedgeprops={'edgecolor': 'w', 'linewidth': 1}
        )

        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Add legend with better formatting
        ax.legend(
            wedges,
            categories.keys(),
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            frameon=True,
            fancybox=True,
            title="Categories"
        )

        # Create canvas with tight layout
        plt.tight_layout()
        self.category_canvas = FigureCanvasTkAgg(self.category_figure, self.category_chart_container)
        self.category_canvas.draw()
        self.category_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_trend_chart(self, transactions):
        # Clear previous chart if exists
        for widget in self.trend_chart_container.winfo_children():
            widget.destroy()

        # Clean up previous matplotlib figure if exists
        if self.trend_figure:
            plt.close(self.trend_figure)

        if not transactions:
            # No transactions to show
            no_data_label = ttk.Label(
                self.trend_chart_container,
                text="No transaction data to display",
                style="Body.TLabel"
            )
            no_data_label.pack(pady=50)
            return

        # Get date range (last 6 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)

        # Create date ranges for each month
        date_ranges = []
        current_date = start_date
        while current_date < end_date:
            month_start = datetime(current_date.year, current_date.month, 1)
            if current_date.month == 12:
                month_end = datetime(current_date.year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = datetime(current_date.year, current_date.month + 1, 1) - timedelta(days=1)

            date_ranges.append((month_start, month_end, month_start.strftime("%b")))

            # Move to next month
            if current_date.month == 12:
                current_date = datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime(current_date.year, current_date.month + 1, 1)

        # Calculate income and expenses for each month
        monthly_income = []
        monthly_expenses = []
        months = []

        for start, end, month_name in date_ranges:
            # Filter transactions for this month
            month_transactions = [t for t in transactions if start <= t.date <= end]

            # Calculate income and expenses
            income = sum(t.amount for t in month_transactions if t.amount > 0)
            expenses = sum(abs(t.amount) for t in month_transactions if t.amount < 0)

            monthly_income.append(income)
            monthly_expenses.append(expenses)
            months.append(month_name)

        # Create bar chart with improved styling
        self.trend_figure, ax = plt.subplots(figsize=(4, 3), dpi=100, facecolor='#f8f9fa')

        x = range(len(months))
        width = 0.35

        # Use more attractive colors
        income_bars = ax.bar([i - width / 2 for i in x], monthly_income, width, label='Income',
                             color='#4ecdc4', edgecolor='white', linewidth=0.7)
        expense_bars = ax.bar([i + width / 2 for i in x], monthly_expenses, width, label='Expenses',
                              color='#ff6b6b', edgecolor='white', linewidth=0.7)

        # Add data labels on top of bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height + 5,
                            f'${height:.0f}', ha='center', va='bottom', fontsize=8)

        add_labels(income_bars)
        add_labels(expense_bars)

        # Improve axis styling
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add grid lines for better readability
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)

        # Add legend with better styling
        ax.legend(frameon=True, fancybox=True)

        # Create canvas with tight layout
        plt.tight_layout()
        self.trend_canvas = FigureCanvasTkAgg(self.trend_figure, self.trend_chart_container)
        self.trend_canvas.draw()
        self.trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_recent_transactions(self, transactions):
        # Clear previous transactions
        for widget in self.transaction_widgets:
            widget.destroy()
        self.transaction_widgets = []

        if not transactions:
            # No transactions to show
            no_data_label = ttk.Label(
                self.transactions_list,
                text="No recent transactions to display",
                style="Body.TLabel"
            )
            no_data_label.pack(pady=20)
            self.transaction_widgets.append(no_data_label)
            return

        # Create header with background
        header_frame = ttk.Frame(self.transactions_list)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Add a subtle header background
        header_bg = ttk.Frame(header_frame, style="Card.TFrame")
        header_bg.place(x=0, y=0, relwidth=1, height=30)

        date_header = ttk.Label(
            header_frame,
            text="Date",
            style="Body.TLabel",
            font=("Helvetica", 12, "bold")
        )
        date_header.pack(side=tk.LEFT, padx=(0, 50))

        desc_header = ttk.Label(
            header_frame,
            text="Description",
            style="Body.TLabel",
            font=("Helvetica", 12, "bold")
        )
        desc_header.pack(side=tk.LEFT, padx=(0, 50))

        amount_header = ttk.Label(
            header_frame,
            text="Amount",
            style="Body.TLabel",
            font=("Helvetica", 12, "bold")
        )
        amount_header.pack(side=tk.RIGHT)

        self.transaction_widgets.append(header_frame)

        # Add a separator after header
        separator = ttk.Separator(self.transactions_list, orient="horizontal")
        separator.pack(fill=tk.X, pady=(0, 5))
        self.transaction_widgets.append(separator)

        # Add transactions with alternating row colors
        for i, transaction in enumerate(transactions):
            # Create a frame with alternating background color
            row_bg_color = "#f5f5f5" if i % 2 == 0 else "#ffffff"
            transaction_frame = ttk.Frame(self.transactions_list)
            transaction_frame.pack(fill=tk.X, pady=5)

            # Add a colored indicator based on transaction type
            indicator_color = "#4ecdc4" if transaction.amount > 0 else "#ff6b6b"
            indicator = tk.Frame(transaction_frame, width=3, background=indicator_color)
            indicator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

            date_label = ttk.Label(
                transaction_frame,
                text=transaction.date.strftime("%m/%d/%Y"),
                style="Body.TLabel"
            )
            date_label.pack(side=tk.LEFT, padx=(0, 50))

            desc_label = ttk.Label(
                transaction_frame,
                text=transaction.description,
                style="Body.TLabel"
            )
            desc_label.pack(side=tk.LEFT, padx=(0, 50))

            # Format amount with color based on type
            amount_color = "#4caf50" if transaction.amount > 0 else "#ef5350"
            amount_text = f"+${transaction.amount:.2f}" if transaction.amount > 0 else f"-${abs(transaction.amount):.2f}"

            amount_label = ttk.Label(
                transaction_frame,
                text=amount_text,
                foreground=amount_color,
                style="Body.TLabel",
                font=("Helvetica", 12, "bold")
            )
            amount_label.pack(side=tk.RIGHT)

            self.transaction_widgets.append(transaction_frame)

            # Add a subtle separator after each row except the last
            if i < len(transactions) - 1:
                row_separator = ttk.Separator(self.transactions_list, orient="horizontal")
                row_separator.pack(fill=tk.X, pady=5)
                self.transaction_widgets.append(row_separator)

    def destroy(self):
        """Properly clean up all resources when the view is destroyed"""
        try:
            # Unbind events
            self.unbind_mousewheel()

            # Clean up matplotlib figures
            self.cleanup_matplotlib_figures()

            # Clean up matplotlib canvases
            if self.category_canvas:
                self.category_canvas.get_tk_widget().destroy()

            if self.trend_canvas:
                self.trend_canvas.get_tk_widget().destroy()

            # Clean up transaction widgets
            for widget in self.transaction_widgets:
                if widget.winfo_exists():
                    widget.destroy()

            # Remove all child widgets
            for widget in self.winfo_children():
                widget.destroy()

            # Call the parent class destroy method
            self.pack_forget()
            ttk.Frame.destroy(self)
        except Exception as e:
            print(f"Error during dashboard view cleanup: {str(e)}")
