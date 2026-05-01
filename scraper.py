import os
import requests
from bs4 import BeautifulSoup

URLS = [
    "https://debales.ai/",
    "https://debales.ai/blog",
]

def scrape_page(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        clean_text = " ".join(text.split())

        return clean_text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def scrape_debales():
    os.makedirs("data", exist_ok=True)
    all_text = ""

    for url in URLS:
        print(f"Scraping: {url}")
        page_text = scrape_page(url)

        if page_text:
            all_text += f"\n\nSource URL: {url}\n"
            all_text += page_text

    with open("data/debales_docs.txt", "w", encoding="utf-8") as file:
        file.write(all_text)

    print("Scraping completed.")
    print("Data saved at: data/debales_docs.txt")

if __name__ == "__main__":
    scrape_debales()