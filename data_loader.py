import pandas as pd
import json
import os
from database import HSNDatabase

class HSNDataLoader:
    """
    Data loader for HSN codes from various sources (CSV, database, JSON).
    """
    
    def __init__(self, source_type="database", source_path=None):
        """
        Initialize the data loader.
        
        Args:
            source_type (str): Type of data source ('database', 'csv', 'json')
            source_path (str): Path to the data source
        """
        self.source_type = source_type.lower()
        self.source_path = source_path
        self.data = None
        self.db = None
        
        # Set default source path if not provided
        if not source_path:
            if source_type == "database":
                self.source_path = "hsn_codes.db"
            elif source_type == "csv":
                self.source_path = os.path.join("Tests", "HSN_codes_cleaned.csv")
            elif source_type == "json":
                self.source_path = "hsn_codes.json"
    
    def load_data(self):
        """
        Load data from the specified source.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.source_type == "database":
                self.db = HSNDatabase(self.source_path)
                self.db.connect()
                return True
            
            elif self.source_type == "csv":
                self.data = pd.read_csv(self.source_path)
                # Ensure column names are correct
                if '\nHSNCode' in self.data.columns:
                    self.data = self.data.rename(columns={'\nHSNCode': 'HSNCode'})
                return True
            
            elif self.source_type == "json":
                with open(self.source_path, 'r') as f:
                    self.data = json.load(f)
                return True
            
            else:
                print(f"Unsupported source type: {self.source_type}")
                return False
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def search_by_code(self, hsn_code):
        """
        Search for HSN codes by code.
        
        Args:
            hsn_code (str): HSN code to search for
        
        Returns:
            list: List of matching records
        """
        if self.source_type == "database" and self.db:
            return self.db.search_by_code(hsn_code)
        
        elif self.source_type == "csv" and self.data is not None:
            # Search in DataFrame
            matches = self.data[self.data['HSNCode'].astype(str).str.startswith(hsn_code)]
            return matches.to_dict('records')
        
        elif self.source_type == "json" and self.data is not None:
            # Search in JSON data
            return [item for item in self.data if item['hsn_code'].startswith(hsn_code)]
        
        return []
    
    def search_by_description(self, description):
        """
        Search for HSN codes by description.
        
        Args:
            description (str): Description to search for
        
        Returns:
            list: List of matching records
        """
        if self.source_type == "database" and self.db:
            return self.db.search_by_description(description)
        
        elif self.source_type == "csv" and self.data is not None:
            # Search in DataFrame (case-insensitive)
            matches = self.data[self.data['Description'].str.contains(description, case=False, na=False)]
            return matches.to_dict('records')
        
        elif self.source_type == "json" and self.data is not None:
            # Search in JSON data (case-insensitive)
            description = description.lower()
            return [item for item in self.data if description in item['description'].lower()]
        
        return []
    
    def is_valid_hsn_code(self, hsn_code):
        """
        Check if an HSN code is valid.
        
        Args:
            hsn_code (str): HSN code to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        if self.source_type == "database" and self.db:
            return self.db.is_valid_hsn_code(hsn_code)
        
        elif self.source_type == "csv" and self.data is not None:
            # Check in DataFrame
            return len(self.data[self.data['HSNCode'].astype(str) == hsn_code]) > 0
        
        elif self.source_type == "json" and self.data is not None:
            # Check in JSON data
            return any(item['hsn_code'] == hsn_code for item in self.data)
        
        return False
    
    def close(self):
        """
        Close any open connections.
        """
        if self.source_type == "database" and self.db:
            self.db.close()