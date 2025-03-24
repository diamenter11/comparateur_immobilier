import pandas as pd
import re
from sqlalchemy import create_engine

# Database connection
engine = create_engine("mysql+pymysql://root:root@localhost/home_investor")

# Load CSV
csv_file_path = "bmc_immo_data.csv"
df = pd.read_csv(csv_file_path)

# Function to extract name, pieces, and size
def extract_details(title):
    try:
        # Example: "Appartement Saint Gratien 4 pièces 61.82 m²"
        match = re.search(r"(.+?)\s(\d+)\spièces\s([\d\.]*)\s?m²?", title)
        
        if match:
            name = match.group(1).strip()
            pieces = int(match.group(2))
            size = float(match.group(3)) if match.group(3) else None
        else:
            # Handle cases where size is missing
            match_no_size = re.search(r"(.+?)\s(\d+)\spièces", title)
            if match_no_size:
                name = match_no_size.group(1).strip()
                pieces = int(match_no_size.group(2))
                size = None
            else:
                name = title.strip()
                pieces = None
                size = None
                
        return name, pieces, size
    
    except Exception as e:
        print(f"Error processing title: {title}, Error: {e}")
        return title, None, None

# Apply function to extract data
df[['Name', 'Pieces', 'Superficie']] = df['Title'].apply(lambda x: pd.Series(extract_details(x)))

# Reorder columns
df = df[['Name', 'Pieces', 'Superficie', 'Price', 'Image', 'Detail Link']]

# Store data in MySQL
df.to_sql('real_estate_listings', con=engine, if_exists='replace', index=False)

print("✅ Data successfully cleaned and stored in MySQL!")

# Display the cleaned DataFrame
print(df.head())
