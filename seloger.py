from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver (Chrome in this case)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the target webpage
url = 'https://www.seloger.com/immobilier/achat/immo-paris-75'  # Replace this with the URL of the page you want to scrape
driver.get(url)

# Give the page time to load dynamically (if necessary)
time.sleep(5)  # Adjust this time depending on how fast the page loads

# Create an empty list to store the extracted data
properties_data = []

# Loop through each property listing on the page
property_listings = driver.find_elements(By.CLASS_NAME, 'listing-class-name')  # Adjust based on your target website

for listing in property_listings:
    try:
        # Extracting the relevant information from each listing
        property_type = listing.find_element(By.CLASS_NAME, 'property-type-class').text.strip()  # Adjust the class name
        price = listing.find_element(By.CLASS_NAME, 'price-class').text.strip()  # Adjust the class name
        size = listing.find_element(By.CLASS_NAME, 'size-class').text.strip()  # Adjust the class name
        location = listing.find_element(By.CLASS_NAME, 'location-class').text.strip()  # Adjust the class name
        main_image_url = listing.find_element(By.TAG_NAME, 'img').get_attribute('src')  # Or use 'data-src' based on the structure
        
        # Store the extracted information in a dictionary
        properties_data.append({
            'Property Type': property_type,
            'Price': price,
            'Size': size,
            'Location': location,
            'Main Image URL': main_image_url
        })
    except Exception as e:
        print(f"Error while extracting data for a property: {e}")
        continue

# Print or process the data
for property in properties_data:
    print(property)

# Close the browser after scraping
driver.quit()
