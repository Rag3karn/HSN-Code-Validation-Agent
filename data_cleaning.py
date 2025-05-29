import pandas as pd
import re
import os

def clean_hsn_data(input_file, output_file=None):
    """
    Clean HSN code dataset by:
    1. Removing rows containing 'other' in description (case-insensitive)
    2. Standardizing HSN codes (removing whitespace, ensuring proper format)
    3. Standardizing descriptions (proper capitalization, removing extra spaces)
    4. Removing duplicates
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str, optional): Path to output CSV file. If None, returns DataFrame
        
    Returns:
        pd.DataFrame or None: Cleaned DataFrame if output_file is None, else None
    """
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Record initial count
    initial_count = len(df)
    print(f"Initial record count: {initial_count}")
    
    # Fix column names (remove any leading/trailing whitespace)
    df.columns = [col.strip() for col in df.columns]
    
    # Rename columns if needed
    if '\nHSNCode' in df.columns:
        df = df.rename(columns={'\nHSNCode': 'HSNCode'})
    
    # 1. Remove rows containing 'other' in description (case-insensitive)
    df_cleaned = df[~df['Description'].str.contains('other', case=False, na=False)]
    other_removed = initial_count - len(df_cleaned)
    print(f"Removed {other_removed} rows containing 'other' in description")
    
    # 2. Standardize HSN codes
    df_cleaned['HSNCode'] = df_cleaned['HSNCode'].astype(str).str.strip()
    
    # 3. Standardize descriptions
    # Remove extra spaces
    df_cleaned['Description'] = df_cleaned['Description'].str.strip()
    df_cleaned['Description'] = df_cleaned['Description'].str.replace('\s+', ' ', regex=True)
    
    # 4. Remove duplicates
    initial_cleaned_count = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()
    duplicates_removed = initial_cleaned_count - len(df_cleaned)
    print(f"Removed {duplicates_removed} duplicate rows")
    
    # Final count
    final_count = len(df_cleaned)
    print(f"Final record count: {final_count}")
    print(f"Total reduction: {initial_count - final_count} rows ({((initial_count - final_count) / initial_count) * 100:.2f}%)")
    
    # Save to file if output_file is provided
    if output_file:
        df_cleaned.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
        return None
    
    return df_cleaned


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output file paths
    input_file = os.path.join(script_dir, "Tests", "HSN codes.csv")
    output_file = os.path.join(script_dir, "Tests", "HSN_codes_cleaned.csv")
    
    # Clean the data
    clean_hsn_data(input_file, output_file)