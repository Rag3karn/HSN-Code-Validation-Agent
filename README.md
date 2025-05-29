# HSN Code Validation Agent

A comprehensive tool for validating and searching Harmonized System Nomenclature (HSN) codes used in international trade and customs.

## Features

- **HSN Code Validation**: Validate HSN codes against a comprehensive database
- **Description Search**: Find HSN codes by searching descriptions
- **Code Extraction**: Extract and validate potential HSN codes from text
- **Hierarchical Validation**: Identify parent categories for invalid codes
- **Interactive Mode**: User-friendly command-line interface


## Setup

### Windows

1. Clone the repository
2. Run the setup script:


### Manual Setup

1. Create a virtual environment:
2. Install dependencies:
3. Setup the database:


## Usage

### Command Line Interface

1. **Validate an HSN code**:
2. **Search for HSN codes by description**:
3. **Extract and validate HSN codes from text**:


### Programmatic Usage

```python
from agent import HSNCodeAgent

# Initialize the agent
agent = HSNCodeAgent()

# Validate an HSN code
result = agent.validate_hsn_code("01011010")
print(result)

# Search by description
results = agent.search_by_description("LIVE HORSES")
print(results)

# Extract codes from text
results = agent.extract_hsn_codes("The shipment contains items with HSN codes 01011010 and 85423100")
print(results)

# Close the agent when done
agent.close()
```


The implementation is now complete! This comprehensive solution includes all the components we discussed:

1. Enhanced data cleaning with standardization steps
2. SQLite database for efficient storage and retrieval
3. Flexible data loader supporting multiple sources
4. HSN Code Validation Agent with validation, search, and extraction capabilities
5. Command-line interface with interactive mode
6. Complete project structure and documentation

You can now run the setup script to initialize the environment and start using the HSN Code Validation Agent.