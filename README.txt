### Budget Manager Application

# README.txt

# Version 1.0.0

# April 27, 2025

## OVERVIEW

Budget Manager is a desktop application built with Python and Tkinter that helps users track their personal finances. The application provides tools for managing income and expenses, categorizing transactions, visualizing spending patterns, and maintaining financial records.

## FEATURES

- User authentication (register, login, logout)
- Transaction management (add, edit, delete)
- Category-based expense tracking
- Financial dashboard with summary statistics
- Data visualization (pie charts, bar graphs)
- Light and dark theme options
- Data export functionality
- Secure password storage using bcrypt


## INSTALLATION

### System Requirements:

- Python 3.10 or higher
- 50MB disk space
- 4GB RAM recommended


### Dependencies:

- matplotlib==3.7.1
- pandas==2.0.1
- pillow==9.5.0
- bcrypt==4.0.1


### Installation Steps:

1. Ensure Python 3.10+ is installed on your system:

```plaintext
python --version
```


2. Download the Budget Manager application files.
3. Install required dependencies:

```plaintext
pip install -r requirements.txt
```


4. Run the application:

```plaintext
python main.py
```




## USAGE

### First-time Setup:

1. Launch the application by running `python main.py`
2. Click "Register" to create a new account
3. Enter your username, email, and password (minimum 6 characters)
4. Log in with your new credentials


### Managing Transactions:

1. From the Dashboard, click "Transactions" in the sidebar
2. Click "+ Add Transaction" to record a new transaction
3. Enter transaction details:

1. Description
2. Amount
3. Category
4. Date



4. Select whether it's an income or expense
5. Click "Save" to add the transaction


### Viewing Financial Summary:

1. Navigate to the Dashboard to see:

1. Total income and expenses
2. Current balance
3. Spending by category (pie chart)
4. Monthly trends (bar chart)
5. Recent transactions





### Customizing Settings:

1. Click "Settings" in the sidebar
2. Change theme between Light and Dark mode
3. Update password if needed
4. Export transaction data to CSV


## FILE STRUCTURE

budget_manager/
├── main.py                  # Application entry point
├── models/                  # Data structures
├── ui/                      # User interface screens
├── controllers/             # Business logic
├── database/                # Database operations
├── utils/                   # Helper functions
└── requirements.txt         # Dependencies

## DATABASE

The application uses SQLite to store data locally on your machine. The database file (budget_manager.db) is created automatically on first run in the application directory.

## TROUBLESHOOTING

### Common Issues:

1. **Application fails to start:**

1. Verify Python version (3.10+)
2. Ensure all dependencies are installed
3. Check for error messages in the console



2. **Registration/Login issues:**

1. If you encounter database errors, try deleting the budget_manager.db file
and restart the application to recreate the database
2. Ensure username is at least 3 characters
3. Ensure password is at least 6 characters



3. **Charts not displaying:**

1. Verify matplotlib is installed correctly
2. Add some transactions to see data visualization



4. **UI rendering problems:**

1. Try switching between light and dark themes
2. Restart the application





### Logs:

Application logs are stored in budget_manager.log in the application directory. Include these logs when reporting issues.

## BACKUP AND RECOVERY

It's recommended to regularly back up your budget_manager.db file to prevent data loss. Simply copy this file to a secure location.

To restore from backup, replace the current database file with your backup copy when the application is not running.

## UPDATES

The application does not currently have an auto-update feature. Check the project repository for new versions and update manually by downloading the latest release.

## LICENSE

This software is released under the MIT License.

## CONTACT AND SUPPORT

For bug reports, feature requests, or general inquiries:

- Email: [support@budgetmanager.example.com](mailto:support@budgetmanager.example.com)
- GitHub: [https://github.com/example/budget-manager](https://github.com/example/budget-manager)


## ACKNOWLEDGMENTS

- Tkinter and ttk for the UI framework
- Matplotlib for data visualization
- SQLite for database management
- Python community for excellent libraries and tools


## DISCLAIMER

This application is provided "as is" without warranty of any kind. Always back up your financial data and do not rely solely on this application for critical financial decisions.