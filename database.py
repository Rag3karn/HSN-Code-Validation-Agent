import sqlite3
import pandas as pd
import os

class HSNDatabase:
    """
    Database handler for HSN codes using SQLite.
    Provides methods for creating, populating, and querying the database.
    """
    
    def __init__(self, db_path="hsn_codes.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """
        Connect to the database.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.conn
    
    def close(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def create_tables(self):
        """
        Create the necessary tables for HSN codes.
        """
        if not self.conn:
            self.connect()
        
        # Create HSN codes table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS hsn_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hsn_code TEXT NOT NULL,
            description TEXT NOT NULL,
            UNIQUE(hsn_code)
        )
        ''')
        
        # Create index for faster searches
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_hsn_code ON hsn_codes(hsn_code)
        ''')
        
        self.conn.commit()
    
    def load_data_from_csv(self, csv_path):
        """
        Load HSN codes from a CSV file into the database.
        
        Args:
            csv_path (str): Path to the CSV file containing HSN codes
        
        Returns:
            int: Number of records inserted
        """
        if not self.conn:
            self.connect()
        
        # Create tables if they don't exist
        self.create_tables()
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Ensure column names are correct
        if '\nHSNCode' in df.columns:
            df = df.rename(columns={'\nHSNCode': 'HSNCode'})
        
        # Insert data into database
        records = 0
        for _, row in df.iterrows():
            try:
                self.cursor.execute(
                    "INSERT OR REPLACE INTO hsn_codes (hsn_code, description) VALUES (?, ?)",
                    (str(row['HSNCode']).strip(), str(row['Description']).strip())
                )
                records += 1
            except Exception as e:
                print(f"Error inserting record: {e}")
        
        self.conn.commit()
        return records
    
    def search_by_code(self, hsn_code):
        """
        Search for HSN codes by exact code or prefix.
        
        Args:
            hsn_code (str): HSN code to search for
        
        Returns:
            list: List of matching records as dictionaries
        """
        if not self.conn:
            self.connect()
        
        # Search for exact match or prefix match
        self.cursor.execute(
            "SELECT hsn_code, description FROM hsn_codes WHERE hsn_code = ? OR hsn_code LIKE ?",
            (hsn_code, f"{hsn_code}%")
        )
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                'hsn_code': row[0],
                'description': row[1]
            })
        
        return results
    
    def search_by_description(self, description):
        """
        Search for HSN codes by description (case-insensitive).
        
        Args:
            description (str): Description to search for
        
        Returns:
            list: List of matching records as dictionaries
        """
        if not self.conn:
            self.connect()
        
        # Search for description (case-insensitive)
        self.cursor.execute(
            "SELECT hsn_code, description FROM hsn_codes WHERE LOWER(description) LIKE LOWER(?)",
            (f"%{description}%",)
        )
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                'hsn_code': row[0],
                'description': row[1]
            })
        
        return results
    
    def is_valid_hsn_code(self, hsn_code):
        """
        Check if an HSN code is valid (exists in the database).
        
        Args:
            hsn_code (str): HSN code to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.conn:
            self.connect()
        
        self.cursor.execute(
            "SELECT COUNT(*) FROM hsn_codes WHERE hsn_code = ?",
            (hsn_code,)
        )
        
        count = self.cursor.fetchone()[0]
        return count > 0