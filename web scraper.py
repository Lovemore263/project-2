import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

# Configure UTF-8 encoding for stdout (Windows-safe)
sys.stdout.reconfigure(encoding='utf-8')

# Set up logging: both to console and to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def scrape_jobs():
    url = "https://vacancymail.co.zw/jobs/"
    try:
        logging.info("Starting job scraping...")

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        job_listings = soup.find_all("div", class_="job-listing-details")
        logging.info(f"Found {len(job_listings)} job listings on the page.")

        if not job_listings:
            logging.warning("No job listings found. The site structure may have changed.")
            return

        job_data = []

        for index, job in enumerate(job_listings[:10], start=1):  # Only first 10 jobs
            logging.info(f"Scraping job #{index}...")
            try:
                title_tag = job.find("h3", class_="job-listing-title")
                desc_tag = job.find("p", class_="job-listing-text")

                if not title_tag or not desc_tag:
                    logging.warning("Missing job title or description. Skipping...")
                    continue

                title = title_tag.get_text(strip=True)
                description = desc_tag.get_text(strip=True)

                footer = job.find_next("div", class_="job-listing-footer")
                footer_items = footer.find_all("li") if footer else []

                location = footer_items[0].get_text(strip=True) if len(footer_items) > 0 else "N/A"
                expiry_date = footer_items[1].get_text(strip=True) if len(footer_items) > 1 else "N/A"

                job_data.append({
                    "Job Title": title,
                    "Company": "Vacancy Mail",
                    "Location": location,
                    "Expiry Date": expiry_date,
                    "Job Description": description
                })

                logging.info(f"Scraped: {title} | Location: {location} | Expires: {expiry_date}")

            except Exception as e:
                logging.error(f"Error scraping a job listing: {e}")

        if job_data:
            df = pd.DataFrame(job_data)
            df.drop_duplicates(inplace=True)
            df.to_csv("scraped_data.csv", index=False)
            logging.info(f"Saved {len(df)} job entries to 'scraped_data.csv'.")
        else:
            logging.warning("No valid job data found.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

# Run the scraper
if __name__ == "__main__":
    scrape_jobs()
