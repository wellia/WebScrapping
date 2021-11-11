import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

GUARDIAN_SEARCH_FILE = 'guardian_search.csv'
GUARDIAN_CONTENT_FILE = 'guardian_content.csv'
SOURCE = "GUARDIAN"

def search_google():
    google_url = "https://google.com/search?q="

    query = 'the guardian australia building defect'  # Fill in google query
    guardian_heading = "https://www.theguardian.com/australia-news"
    query = urllib.parse.quote_plus(query)
    link = google_url + query

    print(f'Main link to search for: {link}')

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path='chromedriver')

    i = 0
    links = []

    n_pages = 2
    for page in range(0, n_pages):
        print('process page:', page)
        link = google_url + query + "&start=" + str((page) * 10)

        driver.get(link)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class = "g"]')))
        headings = driver.find_elements(By.XPATH, '//div[@class = "g"]')  # Heading elements

        for heading in headings:
            title = heading.find_element(By.TAG_NAME, 'h3')
            link = heading.find_element(By.CSS_SELECTOR,'.yuRUbf>a').get_attribute("href")  # This ain't working either, any help?
            if guardian_heading in link:
                links.append(link)

    print(len(links))

    df_search_guardian = pd.DataFrame(links, columns=['site_url'])
    df_search_guardian.to_csv(GUARDIAN_CONTENT_FILE, index=False)

    driver.quit()

def process_content():
    # Get urls that we want to extract the content from
    df_site = pd.read_csv(GUARDIAN_SEARCH_FILE)
    site_urls = df_site['site_url']

    # get site urls
    # Get content    
    content_dicts = []

    i = 1
    for site_url in site_urls:
        page = requests.get(site_url)
        print('Process',i)
        i = i + 1
        news_content = BeautifulSoup(page.content, "html.parser")

        # get title
        title = news_content.title.text

        # get published date
        published_date_el = news_content.find("meta", property="article:published_time")
        if published_date_el:
            published_date = published_date_el["content"][0:10]

        # get tags
        tags = news_content.find_all("meta", property="article:tag")
        news_tags = []
        for tag in tags:
            news_tags.append(tag["content"])
        tag_string = ','.join(map(str, news_tags))

        # get content in text
        news_elements = news_content.find_all("p", class_="dcr-o5gy41")
        news_text = ""
        for news_el in news_elements:
            news_text = news_text + news_el.text + "\n\n"
        
        content_dict = [date.today(), SOURCE, site_url, published_date, title, news_text, tag_string]
        content_dicts.append(content_dict)

    # save results to csv
    df_content = pd.DataFrame(content_dicts, columns=['created_date', 'source', 'site_url',	'published_date', 'title', 'content', 'tags'])
    df_content.to_csv(GUARDIAN_CONTENT_FILE, header = True, index=False)

def main():
    #search_google()
    process_content()

if __name__ == "__main__":
    main()