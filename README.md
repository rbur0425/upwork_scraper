# Upwork Profile Scraper

This script allows you to scrape Upwork profiles based on specific queries. It fetches details like name, headline, body, profile image source, hourly rate, country, total hours, and profile URL.

## Prerequisites

- **Python 3.x**
- **ChromeDriver**: You need to install this on your own. Ensure it matches your Chrome browser version.

## Dependencies

Before running the script, you need to install the required Python packages. You can do this using pip:

```bash
pip install selenium beautifulsoup4 argparse
```

## Usage

To run the script, use the following command:

```
python main.py -q "your_query_here" -num_pages 5 --top-rated-plus --top-rated --rising-talent
```

## Arguments

- -q or --query: Comma-separated list of queries. (Required)
- -num_pages: Number of pages to scrape for each query. (Default is 5)
- --top-rated-plus: Filter for top-rated plus profiles.
- --top-rated: Filter for top-rated profiles.
- --rising-talent: Filter for rising talent profiles.

## Notes

- Ensure that the ChromeDriver is in the same directory as the script or provide the appropriate path in the script.
- The script will create a CSV file for each query with the scraped data.
- If the country is not found for a profile, it defaults to "USA".

## Disclaimer

Web scraping might be against the terms of service of some websites. Always ensure you have the right to scrape a website and be respectful by not hitting the website with too many requests in a short amount of time.
