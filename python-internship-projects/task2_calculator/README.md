# Task 2: Simple Calculator

A modern, responsive calculator supporting basic arithmetic operations, keyboard inputs, calculations history logging, and theme switching.

## Features

- **Double-Mode Interface**: Runs in CLI mode or high-quality GUI.
- **Arithmetic Operations**: Addition, subtraction, multiplication, and division.
- **Additional Functions**: Backspace key (⌫), sign toggler (±), percentage calculation (%).
- **Calculation History**: Collapsible side panel tracking past calculation logs with an option to clear.
- **Keyboard Support**: Control calculations using number keys, operators (`+`, `-`, `*`, `/`), `Return` (`=`), `BackSpace`, and `Escape` (clear).
- **Graceful Error Handling**: Detects and displays errors (e.g. division by zero) without crashing.
- **Theme Customization**: Simple theme toggle between Dark and Light mode.

---

## How to Run

Navigate to the project root directory first.

### Run CLI version
```bash
python task2_calculator/cli.py
```

### Run GUI version
```bash
python task2_calculator/main.py
```

*Note: The GUI version requires `customtkinter`. Ensure dependencies are installed via `pip install -r requirements.txt`.*
