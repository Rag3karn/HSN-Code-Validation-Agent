# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install required packages
pip install pandas numpy jupyter

# Verify installations
python -c "import pandas; import numpy; import jupyter; print('All packages installed successfully!')"

Set-Location "C:\Users\karng\Desktop\HSN-Code-Validation-Agent" 