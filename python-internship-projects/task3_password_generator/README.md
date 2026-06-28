# Task 3: Password Generator

A secure password generation application supporting user-defined lengths, complexity filters, cryptographic security, real-time password strength estimation, and clip-to-clipboard integration.

## Features

- **Double-Mode Interface**: Enjoy either a clean interactive Command Line Interface (CLI) or a modern, sleek Graphical User Interface (GUI).
- **Cryptographically Secure**: Uses Python's standard `secrets` library (designed for security) instead of `random`.
- **Customizable Length**: Generates passwords of any length (from 6 to 48 in GUI; up to 128 in CLI).
- **Complexity Control**: Selectively toggle lowercase (a-z), uppercase (A-Z), numbers (0-9), and symbols (e.g. `!@#$`).
- **Live Strength Estimator**: Dynamically calculates and displays password strength (Weak, Medium, Strong, Very Strong) with a color-coded bar.
- **Copy-to-Clipboard**: Copy generated passwords instantly to clipboard with visual confirmation.

---

## How to Run

Navigate to the project root directory first.

### Run CLI version
```bash
python task3_password_generator/cli.py
```

### Run GUI version
```bash
python task3_password_generator/main.py
```

*Note: The GUI version requires `customtkinter`. Ensure dependencies are installed via `pip install -r requirements.txt`.*
