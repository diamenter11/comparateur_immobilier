from citya import scrape_citya
#from citya import save_to_mysql
from citya import insert_csv_to_mysql
from treatment import process_data_from_db

if __name__ == "__main__":
    #    try:
    #        print("Starting the scraping process...")
    #        df = scrape_citya()
    #        print(df)
        
    #        if df.empty:
    #            print("No data scraped, nothing to save.")
    #        else:
    #            print("Saving data to MySQL...")
    #            insert_csv_to_mysql()
                df = process_data_from_db()

    #            print("Data scraped and saved successfully:")
    #            print(df)
    
    #    except Exception as e:
    #        print(f"An error occurred: {e}")
