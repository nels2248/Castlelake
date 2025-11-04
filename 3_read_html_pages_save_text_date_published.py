import os 
import pandas as pd
from bs4 import BeautifulSoup

# Folder where HTML files are stored
html_dir = "blog_html"

# Lists to store data
contents = []
dates = []
filenames = []

# Loop through each HTML file
for filename in os.listdir(html_dir):
    if not filename.endswith(".html"):
        continue

    filepath = os.path.join(html_dir, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        # Extract blog content
        content_div = soup.find("article", class_="post-type-article")
        content_text = content_div.get_text(separator="\n", strip=True) if content_div else ""

        # Extract publish date from <time> tag
        time_tag = soup.find("time")
        date_text = time_tag.get_text(strip=True) if time_tag else ""

        contents.append(content_text)
        dates.append(date_text)
        filenames.append(filename)

# Create DataFrame
df = pd.DataFrame({
    "filename": filenames,
    "published_date": dates,
    "content": contents
})

# Save to Excel (or CSV if preferred)
df.to_excel("castlelake_blog_content.xlsx", index=False)

print(f"✅ Extracted {len(df)} blog posts into 'castlelake_blog_content.xlsx'")
