import sys

def get_number(prompt):
    while True:
        try:
            val = input(prompt).strip()
            # Support both integer and floating-point inputs
            return float(val) if '.' in val or 'e' in val.lower() else int(val)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_operation():
    operations = {
        '+': 'Addition',
        '-': 'Subtraction',
        '*': 'Multiplication',
        '/': 'Division'
    }
    while True:
        print("\nAvailable Operations:")
        for op, name in operations.items():
            print(f"  {op} : {name}")
        
        choice = input("Enter operation choice (+, -, *, /): ").strip()
        if choice in operations:
            return choice
        else:
            print("Invalid operator. Please choose a valid operation.")

def perform_calculation(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return num1 / num2
    else:
        raise ValueError(f"Unknown operator: {operator}")

def main():
    print("=" * 50)
    print("           SIMPLE PYTHON CALCULATOR CLI           ")
    print("=" * 50)
    
    while True:
        # Prompt user to input two numbers
        num1 = get_number("\nEnter the first number: ")
        num2 = get_number("Enter the second number: ")
        
        # Prompt user to select an operation
        operator = get_operation()
        
        # Perform calculation
        try:
            result = perform_calculation(num1, num2, operator)
            # Format output: if result is equivalent to integer, print as int
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            print(f"\nResult: {num1} {operator} {num2} = {result}")
        except ZeroDivisionError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            
        # Ask to repeat
        choice = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if choice != 'y':
            print("\nThank you for using Simple Calculator. Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main()
