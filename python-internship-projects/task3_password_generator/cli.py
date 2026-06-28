import sys
import string
import secrets

def get_int_input(prompt, min_val=4, max_val=128):
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Please enter a length between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_yes_no(prompt, default='y'):
    while True:
        choice = input(prompt).strip().lower()
        if not choice:
            return default == 'y'
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'.")

def generate_password(length, use_lower, use_upper, use_digits, use_symbols):
    # Construct character sets
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation  # contains symbols like !@#$%^&*()_+...
        
    if not charset:
        raise ValueError("At least one character set must be selected.")
        
    # Generate password cryptographically securely
    password = []
    
    # Ensure at least one character of each selected set is in the password to guarantee complexity
    if use_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_symbols:
        password.append(secrets.choice(string.punctuation))
        
    # Fill up the rest of the password length
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(secrets.choice(charset) for _ in range(remaining_length))
        
    # Shuffle the characters cryptographically securely to avoid starting with predictable types
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)

def main():
    print("=" * 50)
    print("        SECURE PASSWORD GENERATOR CLI        ")
    print("=" * 50)
    
    while True:
        # Prompt length
        length = get_int_input("\nEnter desired password length (4-128, recommended: 12+): ", min_val=4, max_val=128)
        
        # Prompt complexity options
        print("\nSpecify password complexity:")
        use_lower = get_yes_no("Include Lowercase Letters (a-z)? (y/n, default: y): ")
        use_upper = get_yes_no("Include Uppercase Letters (A-Z)? (y/n, default: y): ")
        use_digits = get_yes_no("Include Numbers (0-9)? (y/n, default: y): ")
        use_symbols = get_yes_no("Include Symbols (e.g. !@#$)? (y/n, default: y): ")
        
        # Validation
        if not (use_lower or use_upper or use_digits or use_symbols):
            print("\nError: You must select at least one character type. Defaulting to lowercase letters.")
            use_lower = True
            
        # Generate password
        try:
            password = generate_password(length, use_lower, use_upper, use_digits, use_symbols)
            
            # Display results
            print("\n" + "-" * 50)
            print(f"Generated Password: {password}")
            print("-" * 50)
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            
        # Ask to repeat
        choice = input("\nGenerate another password? (y/n): ").strip().lower()
        if choice != 'y':
            print("\nThank you for using Secure Password Generator. Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main()
