from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from sqlalchemy import create_engine

# Set up Selenium WebDriver
chrome_driver_path = r"C:\Users\natha\Desktop\home-investor\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(service=service, options=options)

# Base URL
base_url = "https://www.bmc-immobilier.fr/a-vendre/appartements/"
data_list = []

# Function to extract details from <h2>
def extract_h2_details(h2_text):
    try:
        parts = h2_text.split(" - ")  # Split by ' - ' to separate location
        property_info = parts[0].split()  # Extract details before location

        property_type = property_info[0]  # First word is the property type
        size = None
        pieces = None

        for word in property_info:
            if "m²" in word:
                size = word.replace("m²", "").strip()
            elif "Pièces" in word:
                pieces = property_info[property_info.index(word) - 1]  # Number before "Pièces"

        location = parts[1] if len(parts) > 1 else None  # Extract location

        return property_type, size, pieces, location
    except Exception as e:
        print(f"Error parsing h2: {h2_text}, Error: {e}")
        return None, None, None, None

# Loop through multiple pages
for page in range(1, 4):  # Pages 1 to 3
    url = f"{base_url}{page}"
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    # Parse the HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all articles
    articles = soup.find_all("article")

    for article in articles:
        # Extract h2 (Title + Info)
        text_block = article.find("div", class_="text-block")
        h2_tag = text_block.find("h2") if text_block else None
        h2_text = h2_tag.get_text(strip=True) if h2_tag else None

        # Extract price
        price_tag = article.find("span", itemprop="price")
        price = price_tag.get_text(strip=True) if price_tag else None

        # Extract Image URL
        img_tag = article.find("img")
        image_url = img_tag["src"] if img_tag else None

        # Extract Details Link
        details_link_tag = article.find("a", href=True)
        details_link = "https://www.bmc-immobilier.fr" + details_link_tag["href"] if details_link_tag else None

        # Extract structured data from h2
        property_type, size, pieces, location = extract_h2_details(h2_text) if h2_text else (None, None, None, None)

        # Append data
        data_list.append([property_type, size, pieces, location, price, image_url, details_link])

# Close Selenium driver
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(data_list, columns=["Property Type", "Size (m²)", "Pieces", "Location", "Price (€)", "Image URL", "Details Link"])

# Save to CSV
df.to_csv("bmc_data.csv", index=False, encoding="utf-8")
print("✅ Data saved to real_estate_data.csv")

# Display DataFrame in terminal
print(df)

# Store in MySQL Database
engine = create_engine("mysql+pymysql://root:root@localhost/home_investor")
df.to_sql("bmc_raw", con=engine, if_exists="replace", index=False)
print("✅ Data stored in MySQL database")
