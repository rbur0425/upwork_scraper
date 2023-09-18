import argparse
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import os

def scrape_upwork_profile(query, num_pages, filename, url_params):
    service = Service(executable_path='./chromedriver')
    driver = webdriver.Chrome(service=service)
    
    results = []

    for page in range(1, num_pages + 1):
        base_url = f'https://www.upwork.com/search/profiles/?page={page}&q={query}'
        full_url = base_url + url_params  # Append the URL parameters
        driver.get(full_url)
        
        tiles = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-test="FreelancerTile"]'))
        )
        
        for tile in tiles:
            tile.click()
            
            time.sleep(15)
            
            profile_url = driver.current_url  # Get the current URL after clicking the tile
            
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            slider_content = soup.find('div', {'tabindex': '-1', 'class': 'up-slider-content'})
            
            name_element = slider_content.find('h1')
            if name_element:
                name = slider_content.find('h1').text.strip()
                headline = slider_content.find('h2').text.strip()
                body = slider_content.find('div', {'data-test': 'up-c-line-clamp'}).text.strip()
                profile_image_src = slider_content.find('img')['src']
                hourly_rate = slider_content.find('span', {'data-test': 'hourly-rate'}).text.strip()
                country_element = slider_content.find('span', {'itemprop': 'country-name'})
                country = country_element.text.strip() if country_element else "USA"  # Default to USA if not found
                total_hours = slider_content.find('div', {'class': 'stat-amount'}).text.strip()
                
                result = {
                    'Name': name,
                    'Headline': headline,
                    'Body': body,
                    'Profile Image Src': profile_image_src,
                    'Hourly Rate': hourly_rate,
                    'Country': country,
                    'Total Hours': total_hours,
                    'Profile URL': profile_url  # Add the profile URL to the results
                }
                results.append(result)
                save_to_csv([result], filename)  # Save the single result to the CSV

            driver.back()
            time.sleep(3)

    driver.close()
    
    return results

def save_to_csv(result, filename):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=result[0].keys())
        if mode == 'w':
            writer.writeheader()
        writer.writerow(result[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Upwork profiles based on queries.')
    parser.add_argument('-q', '--query', help='Comma-separated list of queries', required=True)
    parser.add_argument('-num_pages', type=int, default=5, help='Number of pages to scrape for each query')
    parser.add_argument('--top-rated-plus', action='store_true', help='Filter for top-rated plus profiles')
    parser.add_argument('--top-rated', action='store_true', help='Filter for top-rated profiles')
    parser.add_argument('--rising-talent', action='store_true', help='Filter for rising talent profiles')
    args = parser.parse_args()

    # Generate the URL parameters based on the provided arguments
    url_params = ""
    filename_suffix = ""
    if args.top_rated_plus:
        url_params += "&top_rated_plus=yes"
        filename_suffix += "_top-rated-plus"
    if args.top_rated:
        url_params += "&top_rated_status=top_rated"
        filename_suffix += "_top-rated"
    if args.rising_talent:
        url_params += "&rising_talent=yes"
        filename_suffix += "_rising-talent"

    queries = args.query.split(',')
    for query in queries:
        query = query.strip()
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{query}{filename_suffix}_{current_datetime}.csv"
        results = scrape_upwork_profile(query, args.num_pages, filename, url_params)