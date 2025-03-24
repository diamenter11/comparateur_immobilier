import pandas as pd
from sqlalchemy import create_engine
import re

def process_data_from_db():
    try:
        # Database connection
        engine = create_engine("mysql+pymysql://root:root@localhost/home_investor")
        input_table_name = "citya_raw"  # Source table
        output_table_name = "processed"  # Target table

        # Load data from the database
        df = pd.read_sql_table(input_table_name, con=engine)
        print(f"Data successfully loaded from table '{input_table_name}'.")

        # Ensure the necessary columns are present
        if 'Size' not in df.columns or 'Price' not in df.columns:
            raise ValueError("Missing required columns 'Size' or 'Price' in the database.")

        # Initialize new columns
        df['Rooms'] = None
        df['Surface'] = None

        # Parsing the 'Size' column
        def parse_size(size_text):
            room_pattern = r"(\d+)\s*pièce"  # Extracts the number of rooms
            surface_pattern = r"([\d.]+)\s*m²"  # Extracts the surface area (with decimal support)

            rooms = None
            surface = None

            if isinstance(size_text, str):
                room_match = re.search(room_pattern, size_text)
                surface_match = re.search(surface_pattern, size_text)

                if room_match:
                    rooms = float(room_match.group(1))  # Convert to float for consistency
                if surface_match:
                    surface = float(surface_match.group(1))  # Extract decimal surface

            return rooms, surface

        df[['Rooms', 'Surface']] = df['Size'].apply(lambda x: pd.Series(parse_size(x)))

        # Handle missing surface or rooms
        df['Rooms'] = df['Rooms'].fillna(0)  # Assume 0 rooms if not specified
        df['Surface'] = df['Surface'].fillna(df['Surface'].mean())  # Replace missing surfaces with the mean surface

        # Ensure 'Price' is numeric
        df['Price'] = df['Price'].replace({r'[^\d.]': ''}, regex=True).astype(float)

        # Calculate Pertinence
        df['Pertinence'] = (
            0.6 * (df['Rooms'] / df['Rooms'].max()) +
            0.4 * (df['Surface'] / df['Surface'].max())
        ).fillna(0)

        # Assign Category
        df['Category'] = pd.qcut(df['Pertinence'], q=[0, 0.3, 0.7, 1.0], labels=['Not Interesting', 'Good', 'Very Good'])

        # Add a 'Source' column
        df['Source'] = 'Citya'

        # Save the processed data back to the database
        df.to_sql(output_table_name, con=engine, if_exists='replace', index=False)
        print(f"Processed data successfully saved to table '{output_table_name}'.")

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
