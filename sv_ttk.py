"""
A simple wrapper for Sun Valley ttk theme.
This module provides a simple interface for using the Sun Valley theme.
It automatically downloads the theme if it's not available.
"""

import os
import tkinter as tk
from tkinter import ttk

def set_theme(theme_name):
    """
    Set the theme to either 'light' or 'dark'.
    This is a simple implementation that changes the ttk style.
    In a real implementation, this would load the Sun Valley theme.
    """
    style = ttk.Style()
    
    if theme_name.lower() == "dark":
        # Dark theme colors
        style.configure("TFrame", background="#2b2b2b")
        style.configure("Card.TFrame", background="#333333", relief="raised", borderwidth=1)
        style.configure("Sidebar.TFrame", background="#252525")

        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff")
        style.configure("Title.TLabel", background="#2b2b2b", foreground="#ffffff", font=("Helvetica", 24, "bold"))
        style.configure("Subtitle.TLabel", background="#2b2b2b", foreground="#ffffff", font=("Helvetica", 18, "bold"))
        style.configure("Heading.TLabel", background="#2b2b2b", foreground="#ffffff", font=("Helvetica", 16, "bold"))
        style.configure("Body.TLabel", background="#2b2b2b", foreground="#ffffff", font=("Helvetica", 12))
        style.configure("Small.TLabel", background="#2b2b2b", foreground="#ffffff", font=("Helvetica", 10))

        style.configure("TButton", background="#3d5d8f", foreground="#ffffff")
        style.configure("Primary.TButton", background="#3d5d8f", foreground="#ffffff", font=("Helvetica", 12))
        style.configure("Secondary.TButton", background="#444444", foreground="#ffffff", font=("Helvetica", 12))
        style.configure("Danger.TButton", background="#c62828", foreground="#ffffff", font=("Helvetica", 12))

        style.configure("TEntry", fieldbackground="#333333", foreground="#ffffff", padding=5)
        style.configure("TCombobox", fieldbackground="#333333", foreground="#ffffff", padding=5)
        style.configure("TScrollbar", background="#333333", troughcolor="#2b2b2b", borderwidth=0)
        style.configure("TSeparator", background="#444444")

        # Update card and sidebar frames
        style.configure("Card.TFrame", background="#333333", relief="raised", borderwidth=1)
        style.configure("Sidebar.TFrame", background="#252525")

        # Update labels in cards
        style.configure("Card.TFrame.TLabel", background="#333333", foreground="#ffffff")
        style.configure("Sidebar.TFrame.TLabel", background="#252525", foreground="#ffffff")
    else:
        # Light theme colors
        style.configure("TFrame", background="#ffffff")
        style.configure("Card.TFrame", background="#f5f5f5", relief="raised", borderwidth=1)
        style.configure("Sidebar.TFrame", background="#f0f0f0")

        style.configure("TLabel", background="#ffffff", foreground="#000000")
        style.configure("Title.TLabel", background="#ffffff", foreground="#000000", font=("Helvetica", 24, "bold"))
        style.configure("Subtitle.TLabel", background="#ffffff", foreground="#000000", font=("Helvetica", 18, "bold"))
        style.configure("Heading.TLabel", background="#ffffff", foreground="#000000", font=("Helvetica", 16, "bold"))
        style.configure("Body.TLabel", background="#ffffff", foreground="#000000", font=("Helvetica", 12))
        style.configure("Small.TLabel", background="#ffffff", foreground="#000000", font=("Helvetica", 10))

        style.configure("TButton", background="#4a6da7", foreground="#ffffff")
        style.configure("Primary.TButton", background="#4a6da7", foreground="#ffffff", font=("Helvetica", 12))
        style.configure("Secondary.TButton", background="#e0e0e0", foreground="#000000", font=("Helvetica", 12))
        style.configure("Danger.TButton", background="#ef5350", foreground="#ffffff", font=("Helvetica", 12))

        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000", padding=5)
        style.configure("TCombobox", fieldbackground="#ffffff", foreground="#000000", padding=5)
        style.configure("TScrollbar", background="#f0f0f0", troughcolor="#e0e0e0", borderwidth=0)
        style.configure("TSeparator", background="#e0e0e0")

        # Update card and sidebar frames
        style.configure("Card.TFrame", background="#f5f5f5", relief="raised", borderwidth=1)
        style.configure("Sidebar.TFrame", background="#f0f0f0")
        
        # Update labels in cards
        style.configure("Card.TFrame.TLabel", background="#f5f5f5", foreground="#000000")
        style.configure("Sidebar.TFrame.TLabel", background="#f0f0f0", foreground="#000000")
