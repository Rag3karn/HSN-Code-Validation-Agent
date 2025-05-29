import argparse
import os
import sys
from data_cleaning import clean_hsn_data
from database import HSNDatabase
from agent import HSNCodeAgent

def setup_database():
    """
    Set up the database with cleaned HSN codes.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output file paths
    input_file = os.path.join(script_dir, "Tests", "HSN codes.csv")
    cleaned_file = os.path.join(script_dir, "Tests", "HSN_codes_cleaned.csv")
    db_path = os.path.join(script_dir, "hsn_codes.db")
    
    # Clean the data if needed
    if not os.path.exists(cleaned_file):
        print("Cleaning HSN codes data...")
        clean_hsn_data(input_file, cleaned_file)
    
    # Create and populate the database
    print("Setting up the database...")
    db = HSNDatabase(db_path)
    db.connect()
    db.create_tables()
    records = db.load_data_from_csv(cleaned_file)
    db.close()
    
    print(f"Database setup complete. {records} records loaded.")
    return db_path

def validate_code(hsn_code, data_source="database", source_path=None):
    """
    Validate an HSN code.
    """
    agent = HSNCodeAgent(data_source, source_path)
    result = agent.validate_hsn_code(hsn_code)
    agent.close()
    return result

def search_description(description, data_source="database", source_path=None):
    """
    Search for HSN codes by description.
    """
    agent = HSNCodeAgent(data_source, source_path)
    results = agent.search_by_description(description)
    agent.close()
    return results

def extract_codes(text, data_source="database", source_path=None):
    """
    Extract and validate HSN codes from text.
    """
    agent = HSNCodeAgent(data_source, source_path)
    results = agent.extract_hsn_codes(text)
    agent.close()
    return results

def interactive_mode(data_source="database", source_path=None):
    """
    Run the agent in interactive mode.
    """
    agent = HSNCodeAgent(data_source, source_path)
    
    print("HSN Code Validation Agent - Interactive Mode")
    print("Enter 'exit' to quit")
    
    while True:
        print("\nOptions:")
        print("1. Validate HSN Code")
        print("2. Search by Description")
        print("3. Extract Codes from Text")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            hsn_code = input("Enter HSN code to validate: ")
            result = agent.validate_hsn_code(hsn_code)
            print("\nValidation Result:")
            print(f"Code: {result['code']}")
            print(f"Valid: {result['valid']}")
            
            if not result['valid']:
                print(f"Reason: {result['reason']}")
                if 'parent_codes' in result:
                    print("\nParent Categories:")
                    for parent in result['parent_codes']:
                        print(f"  {parent['hsn_code']}: {parent['description']}")
            else:
                print(f"Description: {result['details']['description']}")
        
        elif choice == "2":
            description = input("Enter description to search for: ")
            results = agent.search_by_description(description)
            print(f"\nFound {len(results)} matching records:")
            for i, result in enumerate(results, 1):
                if isinstance(result, dict):
                    if 'hsn_code' in result:
                        code = result['hsn_code']
                        desc = result['description']
                    else:
                        code = result.get('HSNCode', 'N/A')
                        desc = result.get('Description', 'N/A')
                    print(f"{i}. {code}: {desc}")
        
        elif choice == "3":
            text = input("Enter text to extract HSN codes from: ")
            results = agent.extract_hsn_codes(text)
            print(f"\nExtracted {len(results)} potential HSN codes:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['code']} - Valid: {result['valid']}")
                if not result['valid']:
                    print(f"   Reason: {result['reason']}")
                else:
                    print(f"   Description: {result['details']['description']}")
        
        elif choice == "4" or choice.lower() == "exit":
            break
        
        else:
            print("Invalid choice. Please try again.")
    
    agent.close()
    print("Exiting interactive mode.")

def main():
    parser = argparse.ArgumentParser(description="HSN Code Validation Agent")
    
    # Define subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the database")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate an HSN code")
    validate_parser.add_argument("code", help="HSN code to validate")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for HSN codes by description")
    search_parser.add_argument("description", help="Description to search for")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract HSN codes from text")
    extract_parser.add_argument("text", help="Text to extract HSN codes from")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Run in interactive mode")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "hsn_codes.db")
    
    # Execute the appropriate command
    if args.command == "setup":
        setup_database()
    
    elif args.command == "validate":
        if not os.path.exists(db_path):
            print("Database not found. Running setup first...")
            setup_database()
        
        result = validate_code(args.code, "database", db_path)
        print(f"Code: {result['code']}")
        print(f"Valid: {result['valid']}")
        
        if not result['valid']:
            print(f"Reason: {result['reason']}")
            if 'parent_codes' in result:
                print("\nParent Categories:")
                for parent in result['parent_codes']:
                    print(f"  {parent['hsn_code']}: {parent['description']}")
        else:
            print(f"Description: {result['details']['description']}")
    
    elif args.command == "search":
        if not os.path.exists(db_path):
            print("Database not found. Running setup first...")
            setup_database()
        
        results = search_description(args.description, "database", db_path)
        print(f"Found {len(results)} matching records:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['hsn_code']}: {result['description']}")
    
    elif args.command == "extract":
        if not os.path.exists(db_path):
            print("Database not found. Running setup first...")
            setup_database()
        
        results = extract_codes(args.text, "database", db_path)
        print(f"Extracted {len(results)} potential HSN codes:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['code']} - Valid: {result['valid']}")
            if not result['valid']:
                print(f"   Reason: {result['reason']}")
            else:
                print(f"   Description: {result['details']['description']}")
    
    elif args.command == "interactive":
        if not os.path.exists(db_path):
            print("Database not found. Running setup first...")
            setup_database()
        
        interactive_mode("database", db_path)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()