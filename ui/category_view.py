import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from controllers.transaction_controller import TransactionController
from utils.logger import Logger


class CategoryView(ttk.Frame):
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

        # Load categories
        self.load_categories()

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

        self.categories_button = tk.Button(
            self.sidebar_frame,
            text="Categories",
            command=lambda: None,  # Already on categories
            bg="#4a6da7",
            fg="white",
            font=("Helvetica", 12),
            width=20,
            height=1,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.categories_button.pack(pady=5, padx=20)

    def create_main_content(self):
        # Header
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.pack(fill=tk.X, padx=20, pady=20)

        self.header_label = ttk.Label(
            self.header_frame,
            text="Categories",
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

        # Category overview
        self.overview_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.overview_frame.pack(fill=tk.X, pady=(0, 20))

        self.overview_title = ttk.Label(
            self.overview_frame,
            text="Spending by Category",
            style="Subtitle.TLabel"
        )
        self.overview_title.pack(padx=20, pady=(15, 10), anchor=tk.W)

        # Chart container
        self.chart_container = ttk.Frame(self.overview_frame)
        self.chart_container.pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)

        # Category details
        self.details_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        self.details_frame.pack(fill=tk.X)

        self.details_title = ttk.Label(
            self.details_frame,
            text="Category Details",
            style="Subtitle.TLabel"
        )
        self.details_title.pack(padx=20, pady=(15, 10), anchor=tk.W)

        # Category details container
        self.details_container = ttk.Frame(self.details_frame)
        self.details_container.pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)

    def load_categories(self):
        try:
            # Clear any existing matplotlib figures
            self._clear_matplotlib_figures()

            # Get user's transactions
            transactions = self.transaction_controller.get_user_transactions(self.user.id)

            # Filter expenses only
            expenses = [t for t in transactions if t.amount < 0]

            if not expenses:
                # No expenses to show
                no_data_label = ttk.Label(
                    self.chart_container,
                    text="No expense data to display",
                    style="Body.TLabel"
                )
                no_data_label.pack(pady=50)

                no_details_label = ttk.Label(
                    self.details_container,
                    text="No category details to display",
                    style="Body.TLabel"
                )
                no_details_label.pack(pady=50)
                return

            # Group by category
            categories = {}
            for t in expenses:
                if t.category in categories:
                    categories[t.category] += abs(t.amount)
                else:
                    categories[t.category] = abs(t.amount)

            # Create pie chart
            self.create_category_chart(categories)

            # Create category details
            self.create_category_details(categories, expenses)

        except Exception as e:
            self.logger.log_error(f"Error loading categories: {str(e)}")

    def create_category_chart(self, categories):
        # Clear previous chart if exists
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # Create a frame for the chart with padding
        chart_frame = ttk.Frame(self.chart_container, padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Create pie chart with improved styling
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100, facecolor='#f8f9fa')

        # Custom colors for better visual appeal
        colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#1a535c', '#f7b801',
                  '#7bdff2', '#b2f7ef', '#f7d6e0', '#2ec4b6', '#e71d36']

        # Create exploded pie chart for better emphasis
        explode = [0.05 if amount / sum(categories.values()) > 0.2 else 0 for amount in categories.values()]

        wedges, texts, autotexts = ax.pie(
            categories.values(),
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            explode=explode,
            colors=colors[:len(categories)],
            wedgeprops={'edgecolor': 'w', 'linewidth': 1, 'antialiased': True}
        )

        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Add title
        ax.set_title('Spending Distribution by Category', fontsize=14, pad=20)

        # Add legend with better formatting
        ax.legend(
            wedges,
            categories.keys(),
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            frameon=True,
            fancybox=True,
            shadow=True,
            title="Categories"
        )

        # Create canvas with tight layout
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add a toolbar for interactive features
        toolbar_frame = ttk.Frame(chart_frame)
        toolbar_frame.pack(fill=tk.X, padx=5)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

    def create_category_details(self, categories, expenses):
        # Clear previous details if exists
        for widget in self.details_container.winfo_children():
            widget.destroy()

        # Calculate total expenses
        total_expenses = sum(categories.values())

        # Create a styled frame for the table
        table_frame = ttk.Frame(self.details_container, style="Card.TFrame", padding=10)
        table_frame.pack(fill=tk.X, pady=10, padx=5)

        # Create table header with styled background
        header_frame = ttk.Frame(table_frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Add a subtle header background
        header_bg = ttk.Frame(header_frame, style="Card.TFrame")
        header_bg.place(x=0, y=0, relwidth=1, height=30)

        headers = ["Category", "Amount", "% of Total", "Last Transaction"]
        widths = [150, 100, 100, 150]

        for i, (header, width) in enumerate(zip(headers, widths)):
            header_label = ttk.Label(
                header_frame,
                text=header,
                style="Body.TLabel",
                font=("Helvetica", 12, "bold")
            )
            header_label.pack(side=tk.LEFT, padx=5)

        # Add a separator after header
        ttk.Separator(table_frame, orient="horizontal").pack(fill=tk.X, pady=(0, 10))

        # Create details table with alternating row colors
        details_table = ttk.Frame(table_frame)
        details_table.pack(fill=tk.X)

        # Sort categories by amount (highest first)
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        # Find last transaction for each category
        last_transactions = {}
        for t in expenses:
            if t.category not in last_transactions or t.date > last_transactions[t.category].date:
                last_transactions[t.category] = t

        # Add rows with alternating background colors
        for i, (category, amount) in enumerate(sorted_categories):
            # Create a frame with alternating background color
            row_bg_color = "#f5f5f5" if i % 2 == 0 else "#ffffff"
            row_frame = ttk.Frame(details_table)
            row_frame.pack(fill=tk.X, pady=2)

            # Add a colored indicator based on percentage of total
            percentage = (amount / total_expenses) * 100
            indicator_color = "#ff6b6b" if percentage > 25 else "#4ecdc4" if percentage > 10 else "#ffe66d"

            indicator = tk.Frame(row_frame, width=4, background=indicator_color)
            indicator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

            # Category with icon based on name
            category_frame = ttk.Frame(row_frame)
            category_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, width=150)

            category_label = ttk.Label(
                category_frame,
                text=category,
                style="Body.TLabel",
            )
            category_label.pack(side=tk.LEFT, anchor=tk.W)

            # Amount with formatted currency
            amount_label = ttk.Label(
                row_frame,
                text=f"${amount:.2f}",
                style="Body.TLabel",
                width=100
            )
            amount_label.pack(side=tk.LEFT, padx=5)

            # Percentage with visual indicator
            percentage_frame = ttk.Frame(row_frame)
            percentage_frame.pack(side=tk.LEFT, padx=5, width=100)

            percentage_label = ttk.Label(
                percentage_frame,
                text=f"{percentage:.1f}%",
                style="Body.TLabel",
            )
            percentage_label.pack(side=tk.LEFT)

            # Last transaction with formatted date
            last_transaction = last_transactions.get(category)
            last_transaction_text = last_transaction.date.strftime("%m/%d/%Y") if last_transaction else "N/A"

            last_transaction_label = ttk.Label(
                row_frame,
                text=last_transaction_text,
                style="Body.TLabel",
                width=150
            )
            last_transaction_label.pack(side=tk.LEFT, padx=5)

        # Add a subtle separator after each row except the last
        if i < len(sorted_categories) - 1:
            ttk.Separator(details_table, orient="horizontal").pack(fill=tk.X, pady=5)

    def _clear_matplotlib_figures(self):
        """Clear all matplotlib figures to prevent memory leaks"""
        # Close all figures
        plt.close('all')

        # Clear chart container
        for widget in self.chart_container.winfo_children():
            widget.destroy()

    def destroy(self):
        # Clear matplotlib figures to prevent memory leaks
        plt.close('all')

        # Destroy all child widgets first
        for widget in self.winfo_children():
            widget.destroy()

        # Call parent destroy method
        self.pack_forget()
        ttk.Frame.destroy(self)
