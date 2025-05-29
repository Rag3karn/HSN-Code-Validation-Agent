import re
from data_loader import HSNDataLoader

class HSNCodeAgent:
    """
    HSN Code Validation Agent for validating and searching HSN codes.
    """
    
    def __init__(self, data_source="database", source_path=None):
        """
        Initialize the HSN Code Agent.
        
        Args:
            data_source (str): Type of data source ('database', 'csv', 'json')
            source_path (str): Path to the data source
        """
        self.loader = HSNDataLoader(data_source, source_path)
        self.loader.load_data()
    
    def validate_hsn_code(self, hsn_code):
        """
        Validate an HSN code.
        
        Args:
            hsn_code (str): HSN code to validate
        
        Returns:
            dict: Validation result with status and details
        """
        # Clean the input
        hsn_code = str(hsn_code).strip()
        
        # Check if the code format is valid (2-8 digits)
        if not re.match(r'^\d{2,8}$', hsn_code):
            return {
                'valid': False,
                'reason': 'Invalid HSN code format. HSN codes should be 2-8 digits.',
                'code': hsn_code
            }
        
        # Check if the code exists in the database
        if self.loader.is_valid_hsn_code(hsn_code):
            # Get details for the code
            results = self.loader.search_by_code(hsn_code)
            return {
                'valid': True,
                'code': hsn_code,
                'details': results[0] if results else None
            }
        
        # If not found, try to find parent codes
        parent_codes = []
        for i in range(2, len(hsn_code), 2):
            parent_code = hsn_code[:i]
            if self.loader.is_valid_hsn_code(parent_code):
                results = self.loader.search_by_code(parent_code)
                if results:
                    parent_codes.append(results[0])
        
        if parent_codes:
            return {
                'valid': False,
                'reason': 'Specific HSN code not found, but parent categories exist.',
                'code': hsn_code,
                'parent_codes': parent_codes
            }
        
        return {
            'valid': False,
            'reason': 'HSN code not found in the database.',
            'code': hsn_code
        }
    
    def search_by_description(self, description):
        """
        Search for HSN codes by description.
        
        Args:
            description (str): Description to search for
        
        Returns:
            list: List of matching records
        """
        return self.loader.search_by_description(description)
    
    def extract_hsn_codes(self, text):
        """
        Extract potential HSN codes from text.
        
        Args:
            text (str): Text to extract HSN codes from
        
        Returns:
            list: List of extracted HSN codes with validation status
        """
        # Pattern for potential HSN codes (2-8 digits)
        pattern = r'\b\d{2,8}\b'
        
        # Find all matches
        matches = re.findall(pattern, text)
        
        # Validate each match
        results = []
        for match in matches:
            validation = self.validate_hsn_code(match)
            results.append(validation)
        
        return results
    
    def close(self):
        """
        Close any open connections.
        """
        self.loader.close()