import tkinter as tk
from utils.logger import Logger


class ThemeManager:
    def __init__(self):
        self.logger = Logger()

        # Set default theme
        self.set_default_theme()

    def set_default_theme(self):
        """Set the default theme for the application."""
        try:
            # Default theme is light
            self.logger.log_info("Default theme set")
        except Exception as e:
            self.logger.log_error(f"Error setting default theme: {str(e)}")

    def set_theme_mode(self, mode):
        """Set the theme mode (light, dark)."""
        try:
            import sv_ttk
            if mode.lower() == "dark":
                sv_ttk.set_theme("dark")
                self.logger.log_info("Theme mode set to dark")
                return True
            else:
                sv_ttk.set_theme("light")
                self.logger.log_info("Theme mode set to light")
                return True
        except Exception as e:
            self.logger.log_error(f"Error setting theme mode: {str(e)}")
            return False
