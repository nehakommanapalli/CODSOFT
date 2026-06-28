import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import string
import secrets
import math

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PasswordGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FlowPass - Password Generator")
        self.geometry("420x560")
        self.resizable(False, False)

        # Variables
        self.password_len = tk.IntVar(value=12)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self.create_layout()
        self.generate_password()

    def create_layout(self):
        # Outer Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="FlowPass Generator", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(20, 15))

        # Output / Password Display Frame
        self.display_frame = ctk.CTkFrame(self.main_frame, fg_color=("white", "#2C3E50"), corner_radius=10)
        self.display_frame.pack(fill="x", padx=20, pady=10)

        self.pwd_entry = ctk.CTkEntry(
            self.display_frame, 
            font=ctk.CTkFont(family="Courier", size=18, weight="bold"),
            fg_color="transparent",
            border_width=0,
            justify="center"
        )
        self.pwd_entry.pack(side="left", fill="x", expand=True, padx=(15, 5), pady=10)
        
        # Copy button
        self.copy_btn = ctk.CTkButton(
            self.display_frame, 
            text="📋 Copy", 
            width=70, 
            height=30,
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side="right", padx=10, pady=10)

        # Strength Indicator Frame
        self.strength_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.strength_frame.pack(fill="x", padx=25, pady=5)

        self.strength_text_label = ctk.CTkLabel(
            self.strength_frame, 
            text="Strength: Strong", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.strength_text_label.pack(side="left")

        self.strength_bar = ctk.CTkProgressBar(self.strength_frame, height=8)
        self.strength_bar.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.strength_bar.set(0.0)

        # Separator line
        self.sep = ctk.CTkLabel(self.main_frame, text="—" * 38, text_color="gray")
        self.sep.pack(pady=5)

        # Settings Panel Frame
        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Length Slider Row
        self.length_label_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.length_label_frame.pack(fill="x", pady=2)
        
        self.len_lbl = ctk.CTkLabel(
            self.length_label_frame, 
            text="Password Length:", 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.len_lbl.pack(side="left")
        
        self.len_val_lbl = ctk.CTkLabel(
            self.length_label_frame, 
            text="12", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2196F3"
        )
        self.len_val_lbl.pack(side="right")

        self.slider = ctk.CTkSlider(
            self.settings_frame, 
            from_=6, 
            to=48, 
            number_of_steps=42, 
            variable=self.password_len,
            command=self.on_slider_change
        )
        self.slider.pack(fill="x", pady=(0, 15))

        # Checkboxes
        self.options_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", pady=5)

        self.cb_lower = ctk.CTkCheckBox(
            self.options_frame, 
            text="Lowercase Letters (a-z)", 
            variable=self.use_lower,
            command=self.update_ui
        )
        self.cb_lower.pack(anchor="w", pady=6)

        self.cb_upper = ctk.CTkCheckBox(
            self.options_frame, 
            text="Uppercase Letters (A-Z)", 
            variable=self.use_upper,
            command=self.update_ui
        )
        self.cb_upper.pack(anchor="w", pady=6)

        self.cb_digits = ctk.CTkCheckBox(
            self.options_frame, 
            text="Numbers (0-9)", 
            variable=self.use_digits,
            command=self.update_ui
        )
        self.cb_digits.pack(anchor="w", pady=6)

        self.cb_symbols = ctk.CTkCheckBox(
            self.options_frame, 
            text="Special Symbols (!@#$)", 
            variable=self.use_symbols,
            command=self.update_ui
        )
        self.cb_symbols.pack(anchor="w", pady=6)

        # Generate Button
        self.generate_btn = ctk.CTkButton(
            self.main_frame, 
            text="Generate Password", 
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            command=self.generate_password
        )
        self.generate_btn.pack(fill="x", padx=20, pady=(10, 20))

    def on_slider_change(self, value):
        self.len_val_lbl.configure(text=str(int(value)))
        self.update_ui()

    def update_ui(self):
        # Prevent selecting zero character types
        if not (self.use_lower.get() or self.use_upper.get() or self.use_digits.get() or self.use_symbols.get()):
            self.cb_lower.select()  # force select lowercase if all cleared
        
        # Calculate password strength mock live
        self.calculate_strength()

    def calculate_strength(self):
        length = self.password_len.get()
        types = sum([self.use_lower.get(), self.use_upper.get(), self.use_digits.get(), self.use_symbols.get()])
        
        # Estimate entropy: log2(charset_size^length)
        charset_size = 0
        if self.use_lower.get(): charset_size += 26
        if self.use_upper.get(): charset_size += 26
        if self.use_digits.get(): charset_size += 10
        if self.use_symbols.get(): charset_size += 32
        
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        # Classify entropy
        if entropy < 40:
            self.strength_text_label.configure(text="Strength: Weak", text_color="#E74C3C")
            self.strength_bar.configure(progress_color="#E74C3C")
            self.strength_bar.set(0.25)
        elif entropy < 60:
            self.strength_text_label.configure(text="Strength: Medium", text_color="#E67E22")
            self.strength_bar.configure(progress_color="#E67E22")
            self.strength_bar.set(0.55)
        elif entropy < 80:
            self.strength_text_label.configure(text="Strength: Strong", text_color="#2ECC71")
            self.strength_bar.configure(progress_color="#2ECC71")
            self.strength_bar.set(0.8)
        else:
            self.strength_text_label.configure(text="Strength: Very Strong", text_color="#27AE60")
            self.strength_bar.configure(progress_color="#27AE60")
            self.strength_bar.set(1.0)

    def generate_password(self):
        length = self.password_len.get()
        
        charset = ""
        mandatory_chars = []
        
        if self.use_lower.get():
            charset += string.ascii_lowercase
            mandatory_chars.append(secrets.choice(string.ascii_lowercase))
        if self.use_upper.get():
            charset += string.ascii_uppercase
            mandatory_chars.append(secrets.choice(string.ascii_uppercase))
        if self.use_digits.get():
            charset += string.digits
            mandatory_chars.append(secrets.choice(string.digits))
        if self.use_symbols.get():
            charset += string.punctuation
            mandatory_chars.append(secrets.choice(string.punctuation))

        # Fill up remainder
        remaining_len = length - len(mandatory_chars)
        if remaining_len > 0:
            mandatory_chars.extend(secrets.choice(charset) for _ in range(remaining_len))

        # Shuffle
        secrets.SystemRandom().shuffle(mandatory_chars)
        pwd = "".join(mandatory_chars)

        # Show in Entry (unlocked, modified, locked)
        self.pwd_entry.configure(state="normal")
        self.pwd_entry.delete(0, tk.END)
        self.pwd_entry.insert(0, pwd)
        self.pwd_entry.configure(state="readonly")
        
        # Reset copy button text in case it said "Copied!"
        self.copy_btn.configure(text="📋 Copy", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        
        self.calculate_strength()

    def copy_to_clipboard(self):
        password = self.pwd_entry.get()
        if not password:
            return
            
        self.clipboard_clear()
        self.clipboard_append(password)
        self.update()
        
        # Micro-interaction: temporarily change text & color of copy button
        self.copy_btn.configure(text="✓ Copied!", fg_color="#2ECC71")
        self.after(2000, self.reset_copy_btn)

    def reset_copy_btn(self):
        # Check if widget still exists before modifying (handles window closing early)
        try:
            self.copy_btn.configure(text="📋 Copy", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        except Exception:
            pass

if __name__ == "__main__":
    app = PasswordGenApp()
    app.mainloop()
