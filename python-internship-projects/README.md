# Python Internship Projects

This repository contains three Python-based projects completed for the internship requirements. Each project features both a Command Line Interface (CLI) version and a modern, high-quality Graphical User Interface (GUI) built with CustomTkinter.

## Repository Structure

```
python-internship-projects/
│
├── README.md                           # Global setup and details
├── requirements.txt                    # List of external dependencies
│
├── task1_todo_list/                    # Task 1: To-Do List Application
│   ├── README.md                       # Setup and features
│   ├── cli.py                          # CLI version
│   ├── gui.py                          # GUI version
│   └── main.py                         # GUI entry point
│
├── task2_calculator/                   # Task 2: Calculator Application
│   ├── README.md                       # Setup and features
│   ├── cli.py                          # CLI version
│   ├── gui.py                          # GUI version
│   └── main.py                         # GUI entry point
│
└── task3_password_generator/           # Task 3: Password Generator Application
    ├── README.md                       # Setup and features
    ├── cli.py                          # CLI version
    ├── gui.py                          # GUI version
    └── main.py                         # GUI entry point
```

---

## Getting Started

### Prerequisites

- **Python**: Make sure Python 3.8+ is installed on your system.
- **Pip**: The Python package manager.

### Installation

1. Clone or download this repository.
2. Navigate to the repository root directory in your terminal:
   ```bash
   cd python-internship-projects
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Applications

### Task 1: To-Do List Application
Manage, categorize, prioritize, and track your daily tasks.
- **Run CLI version**:
  ```bash
  python task1_todo_list/cli.py
  ```
- **Run GUI version**:
  ```bash
  python task1_todo_list/main.py
  ```

### Task 2: Simple Calculator
Perform basic arithmetic operations with an interactive interface.
- **Run CLI version**:
  ```bash
  python task2_calculator/cli.py
  ```
- **Run GUI version**:
  ```bash
  python task2_calculator/main.py
  ```

### Task 3: Password Generator
Generate secure and customizable random passwords.
- **Run CLI version**:
  ```bash
  python task3_password_generator/cli.py
  ```
- **Run GUI version**:
  ```bash
  python task3_password_generator/main.py
  ```

---

## Features Summary

| Project | CLI Features | GUI Features |
| :--- | :--- | :--- |
| **To-Do List** | Add, View, Complete, Delete, JSON Persistence | Dashboard, Search, Priority Tags, Category Filters, Completion Progress Bar, JSON Persistence |
| **Calculator** | Standard Operators, Divide-by-Zero Protection | Sleek Glassmorphism Grid, Dynamic expression log, Calculation History, Keyboard Bindings |
| **Password Generator** | Length Input, Character Class Flags, Secrets Module | Slider Length Control, Complexity Selectors, Real-time Strength Meter, Copy-to-Clipboard |
