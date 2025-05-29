# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install required packages
pip install -r requirements.txt

# Set up the database
python main.py setup

# Verify installations
python -c "import pandas; import numpy; import sqlite3; print('All packages installed successfully!')"

Write-Host "Environment setup complete. You can now use the HSN Code Validation Agent."
Write-Host "To run the agent in interactive mode, use: python main.py interactive"

Set-Location "C:\Users\karng\Desktop\HSN-Code-Validation-Agent"