🧰 Job Scraper for VacancyMail
This Python script scrapes the latest job postings from vacancymail.co.zw and saves them into a CSV file. It uses requests for fetching the webpage, BeautifulSoup for parsing HTML, and pandas for data manipulation.

📦 Features
Scrapes up to the first 10 job listings from the VacancyMail jobs page.

Extracts:

Job Title

Company (default: Vacancy Mail)

Location

Expiry Date

Job Description

Saves the data in a CSV file (scraped_data.csv).

Includes logging for tracking the scraping process and any potential issues.

🛠️ Requirements
Install the following Python packages if you don't already have them:

bash
Copy
Edit
pip install requests beautifulsoup4 pandas
🚀 How to Run
Make sure you have Python 3 installed.

Clone or download this repository.

Run the script:

bash
Copy
Edit
python job_scraper.py
Note: The script is named job_scraper.py in this example—rename your file accordingly if needed.

📁 Output
A file named scraped_data.csv will be created in the same directory, containing the scraped job data.

⚠️ Disclaimer
This script relies on the current structure of the vacancymail.co.zw website. If the site structure changes, the scraper may stop working and will need to be updated.

✅ Example Output

Job Title	Company	Location	Expiry Date	Job Description
Software Developer	Vacancy Mail	Harare	20 Apr 2025	Responsible for web development
Accountant	Vacancy Mail	Bulawayo	25 Apr 2025	Handles financial records
