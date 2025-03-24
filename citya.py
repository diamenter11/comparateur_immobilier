



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import pandas as pd
# import time

# # Path to ChromeDriver
# chrome_driver_path = r"C:\Users\natha\Desktop\home-investor\chromedriver-win64\chromedriver.exe"
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service)

# # Base URL
# base_url = "https://www.citya.com/annonces/vente/appartement/paris-75?sort=b.dateMandat&direction=desc"
# pages_to_scrape = 2  # Number of pages

# properties = []

# for page_num in range(1, pages_to_scrape + 1):
#     url = f"{base_url}&page={page_num}"
#     driver.get(url)
#     time.sleep(5)  # Wait for dynamic content to load
    
#     # Extract HTML with Selenium
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
    
#     articles = soup.find_all('article')  # Find all articles
#     for article in articles:
#         try:
#             # Extract data using Beautiful Soup
#             image_src = article.find('img')['src']
#             info_href = article.find('a', {'title': True})['href']
#             size = article.find('h3').find('strong').get_text(strip=True)
#             price = article.find('p', class_='prix').find('strong').get_text(strip=True)

#             properties.append({
#                 "Price": price,
#                 "Size": size,
#                 "Image Source": f"https://www.citya.com{image_src}",
#                 "Info Link": f"https://www.citya.com{info_href}"
#             })
#         except Exception as e:
#             print(f"Error scraping article: {e}")

# driver.quit()

# # Save to CSV
# df = pd.DataFrame(properties)
# df.to_csv('citya_hybrid.csv', index=False)
# print(df)











from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time


import pymysql
from sqlalchemy import create_engine

def scrape_citya():
    """
    Scrapes property data from the Citya website.
    The function is fully autonomous and does not require parameters.
    It saves the scraped data to a CSV file and returns a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing scraped property data.
    """
    # Configuration interne
    chrome_driver_path = r"C:\Users\natha\Desktop\home-investor\chromedriver-win64\chromedriver.exe"
    base_url = "https://www.citya.com/annonces/vente/appartement/paris-75?sort=b.dateMandat&direction=desc"
    pages_to_scrape = 2  # Nombre de pages à scrapper
    output_file = 'citya_hybrid.csv'

    # Initialisation de WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    properties = []

    try:
        for page_num in range(1, pages_to_scrape + 1):
            url = f"{base_url}&page={page_num}"
            driver.get(url)
            time.sleep(5)  # Attente pour le chargement du contenu dynamique

            # Extraction du HTML avec Selenium et analyse avec Beautiful Soup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            articles = soup.find_all('article')  # Trouve tous les articles

            for article in articles:
                try:
                    # Extraction des données avec Beautiful Soup
                    image_src = article.find('img')['src']
                    info_href = article.find('a', {'title': True})['href']
                    size = article.find('h3').find('strong').get_text(strip=True)
                    price = article.find('p', class_='prix').find('strong').get_text(strip=True)

                    properties.append({
                        "Price": price,
                        "Size": size,
                        "Image Source": f"https://www.citya.com{image_src}",
                        "Info Link": f"https://www.citya.com{info_href}"
                    })
                except Exception as e:
                    print(f"Error scraping article: {e}")

    finally:
        driver.quit()

    # Sauvegarde des données dans un fichier CSV
    df = pd.DataFrame(properties)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    return df










def insert_csv_to_mysql():
    csv_file_path = r"C:\Users\natha\Desktop\home-investor\citya_hybrid.csv"  # Path to CSV
    table_name = "citya_raw"  # Table name in MySQL
    try:
        # Read data from CSV
        df = pd.read_csv(csv_file_path)
        print(f"CSV file '{csv_file_path}' successfully read!")

        # Create a connection to the database
        engine = create_engine("mysql+pymysql://root:root@localhost/home_investor")

        # Insert data into the MySQL table
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Data successfully inserted into MySQL table '{table_name}'.")

    except Exception as e:
        print(f"Error inserting data into MySQL: {e}")








