import sys
import os

try:
    # Add current directory to path just in case
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    import customtkinter as ctk
    from gui import CalculatorApp

    if __name__ == "__main__":
        app = CalculatorApp()
        app.mainloop()

except ModuleNotFoundError:
    import tkinter as tk
    from tkinter import messagebox
    
    # Suppress main window
    root = tk.Tk()
    root.withdraw()
    
    error_msg = (
        "Dependency Missing: 'customtkinter' module was not found.\n\n"
        "To run the modern GUI version, please install the dependencies:\n"
        "pip install -r requirements.txt\n\n"
        "Alternatively, you can run the command-line version:\n"
        "python cli.py"
    )
    
    print("\n" + "!" * 60)
    print("Missing dependency: customtkinter")
    print("Please run: pip install -r requirements.txt")
    print("!" * 60 + "\n")
    
    messagebox.showerror("Dependency Error", error_msg)
    sys.exit(1)
