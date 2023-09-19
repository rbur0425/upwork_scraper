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
    profile_keys = []

    for page in range(1, num_pages + 1):
        base_url = f'https://www.upwork.com/search/profiles/?page={page}&q={query}'
        full_url = base_url + url_params
        driver.get(full_url)
        
        tiles = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-test="FreelancerTile"]'))
        )

        # Take a screenshot and save it
        screenshot_filename = f"screenshot_{query}_page_{page}.png"
        driver.save_screenshot(screenshot_filename)
        
        time.sleep(2)
        for tile in tiles:
            profile_key = tile.get_attribute('data-test-key').replace('null', '')
            profile_keys.append(profile_key)

    for key in profile_keys:
        profile_url = f'https://www.upwork.com/freelancers/{key}'
        driver.get(profile_url)
        time.sleep(15)
        
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        main = soup.find('div', {'class': 'container'})
        
        name_element = main.find('h1', {'itemprop': 'name'})
        print(name_element)
        if name_element:
            name = name_element.text.strip()
            headline = main.find('h2').text.strip()
            body = main.find('span', {'class': 'text-pre-line break'}).text.strip()
            profile_image_src = main.find('img')['src']
            hourly_rate = main.find('h3', {'role': 'presentation', 'class': 'd-inline font-weight-black'}).span.text.strip()
            country_element = main.find('span', {'itemprop': 'country-name'})
            country = country_element.text.strip() if country_element else "USA"
            total_hours = main.find('div', {'class': 'stat-amount'}).text.strip()
            
            result = {
                'Name': name,
                'Headline': headline,
                'Body': body,
                'Profile Image Src': profile_image_src,
                'Hourly Rate': hourly_rate,
                'Country': country,
                'Total Hours': total_hours,
                'Profile URL': profile_url
            }
            print(result)
            results.append(result)
            save_to_csv([result], filename)

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
