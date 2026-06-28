import tkinter as tk
import customtkinter as ctk
import math

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FlowCalc - Simple Calculator")
        self.geometry("380x580")
        self.resizable(False, False)

        # Internal state
        self.expression = ""
        self.current_value = "0"
        self.history = []
        self.show_history = False
        self.reset_on_next_input = False

        # Key mappings for keyboard inputs
        self.bind("<Key>", self.handle_key_press)
        
        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_layout()

    def create_layout(self):
        # Master container frame containing calculator + history side-by-side
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)  # Calc panel
        
        # Calculator main panel
        self.calc_panel = ctk.CTkFrame(self.container, corner_radius=15)
        self.calc_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.calc_panel.grid_columnconfigure(0, weight=1)
        self.calc_panel.grid_rowconfigure(2, weight=1)

        # Top Control Row (History toggle)
        self.top_row = ctk.CTkFrame(self.calc_panel, fg_color="transparent", height=30)
        self.top_row.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        
        self.history_btn = ctk.CTkButton(
            self.top_row, 
            text="📜 History", 
            width=80, 
            height=26,
            fg_color="#34495E",
            hover_color="#2C3E50",
            command=self.toggle_history
        )
        self.history_btn.pack(side="left")

        self.theme_btn = ctk.CTkButton(
            self.top_row, 
            text="🌓 Theme", 
            width=80, 
            height=26,
            fg_color="#34495E",
            hover_color="#2C3E50",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right")

        # Display Frame
        self.display_frame = ctk.CTkFrame(self.calc_panel, fg_color=("white", "#2C3E50"), corner_radius=10)
        self.display_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=10)
        
        self.expr_label = ctk.CTkLabel(
            self.display_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="gray",
            anchor="e"
        )
        self.expr_label.pack(fill="x", padx=15, pady=(8, 0))

        self.value_label = ctk.CTkLabel(
            self.display_frame,
            text="0",
            font=ctk.CTkFont(size=36, weight="bold"),
            anchor="e"
        )
        self.value_label.pack(fill="x", padx=15, pady=(0, 8))

        # Button Grid Frame
        self.buttons_frame = ctk.CTkFrame(self.calc_panel, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(5, 15))

        # Grid row/col configure for buttons
        for r in range(5):
            self.buttons_frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.buttons_frame.grid_columnconfigure(c, weight=1)

        # Button Layout
        buttons_layout = [
            ("C", 0, 0, "#E74C3C", "#C0392B"), ("⌫", 0, 1, "#7F8C8D", "#95A5A6"), ("%", 0, 2, "#34495E", "#2C3E50"), ("/", 0, 3, "#2980B9", "#1F618D"),
            ("7", 1, 0, None, None),            ("8", 1, 1, None, None),            ("9", 1, 2, None, None),            ("*", 1, 3, "#2980B9", "#1F618D"),
            ("4", 2, 0, None, None),            ("5", 2, 1, None, None),            ("6", 2, 2, None, None),            ("-", 2, 3, "#2980B9", "#1F618D"),
            ("1", 3, 0, None, None),            ("2", 3, 1, None, None),            ("3", 3, 2, None, None),            ("+", 3, 3, "#2980B9", "#1F618D"),
            ("±", 4, 0, None, None),            ("0", 4, 1, None, None),            (".", 4, 2, None, None),            ("=", 4, 3, "#27AE60", "#2196F3")
        ]

        # Draw buttons
        for text, r, c, bg, hover in buttons_layout:
            self.create_calc_button(text, r, c, bg, hover)

        # Create history panel (initially detached/hidden in layout)
        self.history_panel = ctk.CTkFrame(self.container, width=200, corner_radius=15)
        self.history_panel.grid_rowconfigure(1, weight=1)
        
        # History title
        self.hist_title = ctk.CTkLabel(
            self.history_panel, 
            text="History Log", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.hist_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # History display box
        self.history_box = ctk.CTkTextbox(
            self.history_panel, 
            width=180, 
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.history_box.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.history_box.configure(state="disabled")

        # Clear history button
        self.clear_hist_btn = ctk.CTkButton(
            self.history_panel,
            text="Clear Log",
            fg_color="#C0392B",
            hover_color="#962D22",
            height=26,
            command=self.clear_history
        )
        self.clear_hist_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def create_calc_button(self, text, r, c, bg=None, hover=None):
        # Default colors
        if bg is None:
            # Number button
            bg = ("#E5E8E8", "#34495E")
            hover = ("#BDC3C7", "#2C3E50")
            text_color = ("black", "white")
        else:
            text_color = "white"

        btn = ctk.CTkButton(
            self.buttons_frame,
            text=text,
            fg_color=bg,
            hover_color=hover,
            text_color=text_color,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=8,
            command=lambda: self.handle_input(text)
        )
        btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

    def handle_input(self, val):
        if val == "C":
            self.clear_screen()
        elif val == "⌫":
            self.backspace()
        elif val == "=":
            self.calculate_result()
        elif val == "±":
            self.toggle_sign()
        elif val == "%":
            self.apply_percentage()
        elif val in ["+", "-", "*", "/"]:
            self.add_operator(val)
        else:
            self.add_digit(val)

    def clear_screen(self):
        self.expression = ""
        self.current_value = "0"
        self.expr_label.configure(text="")
        self.value_label.configure(text="0")
        self.reset_on_next_input = False

    def backspace(self):
        if self.reset_on_next_input:
            self.clear_screen()
            return
            
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
        self.value_label.configure(text=self.current_value)

    def toggle_sign(self):
        if self.current_value == "0":
            return
            
        if self.current_value.startswith("-"):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = "-" + self.current_value
            
        self.value_label.configure(text=self.current_value)

    def apply_percentage(self):
        try:
            val = float(self.current_value) / 100
            self.current_value = self.format_output(val)
            self.value_label.configure(text=self.current_value)
            self.reset_on_next_input = True
        except ValueError:
            pass

    def add_operator(self, op):
        if self.reset_on_next_input:
            self.expression = self.current_value + " " + op + " "
            self.reset_on_next_input = False
        else:
            # If current value is entered, build operator expression
            self.expression += self.current_value + " " + op + " "
            
        self.expr_label.configure(text=self.expression)
        self.current_value = "0"
        self.value_label.configure(text="0")

    def add_digit(self, char):
        if self.reset_on_next_input:
            self.clear_screen()
            self.reset_on_next_input = False

        if char == ".":
            if "." in self.current_value:
                return  # Block duplicate decimals
            self.current_value += "."
        elif self.current_value == "0":
            self.current_value = char
        else:
            self.current_value += char

        self.value_label.configure(text=self.current_value)

    def calculate_result(self):
        if not self.expression:
            return

        full_expr = self.expression + self.current_value
        # Replace display operators with python math equivalents
        eval_expr = full_expr.replace("x", "*").replace("÷", "/")
        
        try:
            # Evaluate the mathematical string safely
            # Note: eval is controlled as only numeric operations can trigger
            res = eval(eval_expr)
            formatted_res = self.format_output(res)
            
            # Update GUI labels
            self.expr_label.configure(text=full_expr + " =")
            self.value_label.configure(text=formatted_res)
            
            # Log history
            hist_item = f"{full_expr}\n= {formatted_res}\n"
            self.history.append(hist_item)
            self.update_history_display()
            
            # Update variables
            self.current_value = formatted_res
            self.expression = ""
            self.reset_on_next_input = True
            
        except ZeroDivisionError:
            self.value_label.configure(text="Error: Div by 0")
            self.reset_on_next_input = True
        except Exception:
            self.value_label.configure(text="Error")
            self.reset_on_next_input = True

    def format_output(self, val):
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        elif isinstance(val, float):
            # Check length to prevent overflow in display
            s = f"{val:.6f}".rstrip("0").rstrip(".")
            if len(s) > 12:
                return f"{val:.4e}"
            return s
        return str(val)

    def handle_key_press(self, event):
        char = event.char
        keysym = event.keysym
        
        if char in "0123456789.":
            self.add_digit(char)
        elif char in "+-*/":
            self.add_operator(char)
        elif char == "=" or keysym == "Return":
            self.calculate_result()
        elif keysym == "BackSpace":
            self.backspace()
        elif keysym == "Escape":
            self.clear_screen()

    def toggle_history(self):
        self.show_history = not self.show_history
        if self.show_history:
            self.geometry("600x580")
            self.history_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            self.history_btn.configure(fg_color="#2C3E50")
        else:
            self.geometry("380x580")
            self.history_panel.grid_forget()
            self.history_btn.configure(fg_color="#34495E")

    def toggle_theme(self):
        current_theme = ctk.get_appearance_mode()
        new_theme = "Light" if current_theme == "Dark" else "Dark"
        ctk.set_appearance_mode(new_theme)

    def update_history_display(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", tk.END)
        for entry in reversed(self.history):
            self.history_box.insert(tk.END, entry + "-"*18 + "\n")
        self.history_box.configure(state="disabled")

    def clear_history(self):
        self.history = []
        self.update_history_display()

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
