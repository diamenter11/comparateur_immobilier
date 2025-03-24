from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# Specify the path to your ChromeDriver
chrome_driver_path = "C:\\Users\\natha\\Desktop\\home-investor\\chromedriver-win64\\chromedriver.exe"

# Set up the ChromeDriver Service
service = Service(executable_path=chrome_driver_path)

# Optionally, set Chrome options (e.g., headless mode)
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
chrome_options.add_argument("--start-maximized")  # Start in full-screen mode
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize the WebDriver with the specified Service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target webpage
url = 'https://www.facebook.com/marketplace/category/propertyforsale'
driver.get(url)

# Wait for the page to load (adjust this as necessary)
time.sleep(10)

# Log in (if necessary)
try:
    login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Log In")]')
    login_button.click()
    time.sleep(5)  # Adjust based on login speed
    # Add steps to input username/password here if required
except Exception as e:
    print(f"No login required or login button not found: {e}")

# Create an empty list to store the extracted data
properties_data = []

# Scroll to load more listings (if necessary)
for _ in range(5):  # Adjust the range for more scrolling
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Extract property listings
try:
    property_listings = driver.find_elements(By.XPATH, '//div[contains(@class, "property-listing-class")]')  # Adjust XPath
    for listing in property_listings:
        try:
            # Extract details for each listing
            property_type = listing.find_element(By.XPATH, './/div[contains(@class, "property-type-class")]').text.strip()
            price = listing.find_element(By.XPATH, './/div[contains(@class, "price-class")]').text.strip()
            size = listing.find_element(By.XPATH, './/div[contains(@class, "size-class")]').text.strip()
            location = listing.find_element(By.XPATH, './/div[contains(@class, "location-class")]').text.strip()
            main_image_url = listing.find_element(By.TAG_NAME, 'img').get_attribute('src')

            # Append extracted data to the list
            properties_data.append({
                'Property Type': property_type,
                'Price': price,
                'Size': size,
                'Location': location,
                'Main Image URL': main_image_url
            })
        except Exception as inner_e:
            print(f"Error extracting a property listing: {inner_e}")
            continue
except Exception as outer_e:
    print(f"Error extracting property listings: {outer_e}")

# Print the extracted data
for property in properties_data:
    print(property)

# Close the browser
driver.quit()
