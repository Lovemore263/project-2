import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_jobs():
    url = "https://vacancymail.co.zw/jobs/"
    try:
        logging.info("Starting job scraping...")

        # Get the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all job listings
        job_listings = soup.find_all("div", class_="job-listing-details")
        logging.info(f"Found {len(job_listings)} job listings.")

        if not job_listings:
            logging.warning("⚠️ No job listings found. Site structure may have changed.")
            return

        job_data = []

        for job in job_listings[:10]:  # Limit to first 10 jobs
            try:
                job_title_tag = job.find("h3", class_="job-listing-title")
                job_description_tag = job.find("p", class_="job-listing-text")

                if not job_title_tag or not job_description_tag:
                    logging.warning("Missing job title or description; skipping entry.")
                    continue

                job_title = job_title_tag.get_text(strip=True)
                job_description = job_description_tag.get_text(strip=True)

                footer = job.find_next("div", class_="job-listing-footer")
                footer_items = footer.find_all("li") if footer else []

                location = footer_items[0].get_text(strip=True) if len(footer_items) > 0 else "N/A"
                expiry_date = footer_items[1].get_text(strip=True) if len(footer_items) > 1 else "N/A"

                company = "Vacancy Mail"

                job_data.append({
                    "Job Title": job_title,
                    "Company": company,
                    "Location": location,
                    "Expiry Date": expiry_date,
                    "Job Description": job_description
                })

            except Exception as e:
                logging.error(f"Error extracting job data: {e}")

        if job_data:
            df = pd.DataFrame(job_data)
            df.drop_duplicates(inplace=True)
            df.to_csv('scraped_data.csv', index=False)
            logging.info("✅ Job data has been saved to 'scraped_data.csv'.")
        else:
            logging.warning("⚠️ No job data to save.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

# Run the scraper
if __name__ == "__main__":
    scrape_jobs()
