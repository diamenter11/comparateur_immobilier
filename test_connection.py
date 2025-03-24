from sqlalchemy import create_engine, text

def test_mysql_connection():
    try:
        # Create engine to connect to the 'home_investor' database
        engine = create_engine("mysql+pymysql://root:root@localhost/home_investor")
        
        # Connect to the engine
        with engine.connect() as connection:
            print("Connection successful!")
            
            # Create a simple test table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS test_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT
            );
            """
            
            # Execute the query to create the table
            connection.execute(text(create_table_query))
            print("Test table created (if it didn't exist already).")
            
            # Insert a sample record into the test table to ensure everything is working
            insert_query = "INSERT INTO test_table (name, age) VALUES ('John Doe', 30)"
            connection.execute(text(insert_query))
            print("Sample data inserted into the test table.")
            
            # Query the table to check the inserted data
            result = connection.execute("SELECT * FROM test_table")
            rows = result.fetchall()
            print("Data in test_table:")
            for row in rows:
                print(row)

    except Exception as e:
        print(f"Error: {e}")

# Run the test function
test_mysql_connection()
