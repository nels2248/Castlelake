import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# Base URL for Castlelake Insights
base_url = "https://www.castlelake.com/insights/"

article_links = []

# Loop through pages 1 to 10
for page in range(1, 11):
    url = f"{base_url}?query-7-page={page}#plaudit_query_results_7"
    print(f"Scraping: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error on page {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags and filter for links containing "/article/"
    for a in soup.find_all("a", href=True):
        href = a["href"]

        # Some links are relative (e.g., /article/...). Convert to full URL.
        if "/article/" in href:
            if href.startswith("/"):
                href = "https://www.castlelake.com" + href
            article_links.append(href)

    time.sleep(1)  # Respectful delay

# Remove duplicates & sort
unique_links = sorted(set(article_links))

# Convert to DataFrame
df = pd.DataFrame(unique_links, columns=["Article Link"])

# Save to Excel
output_file = "castlelake_insights_article_links.xlsx"
df.to_excel(output_file, index=False)

print(f"\n✅ Saved {len(unique_links)} article links to '{output_file}'")