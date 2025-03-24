import requests
from bs4 import BeautifulSoup

def get_hotel_emails(city):
    url = f"https://www.google.com/search?q=hotels+{city}+email"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    emails = set()
    for link in soup.find_all("a", href=True):
        if "mailto:" in link["href"]:
            emails.add(link["href"].replace("mailto:", ""))

    return list(emails)

hotels_corbeil = get_hotel_emails("Corbeil-Essonnes")
hotels_paris = get_hotel_emails("Paris")

all_emails = hotels_corbeil + hotels_paris
print(all_emails)
