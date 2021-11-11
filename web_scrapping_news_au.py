# -------- Currently under development --------
# Purpose to control objects on a webpage, so we can login and sort the news
# ---------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import traceback
from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

NEWS_AU_SEARCH_FILE = 'news_au_search.csv'
# DAILY_TEL_SEARCH_FILE = 'daily_tel_search.csv'
# ADELAIDE_SEARCH_FILE = 'adelaide_search.csv'

NEWS_AU_CONTENT_FILE = 'news_au_content.csv'
# DAILY_TEL_CONTENT_FILE = 'daily_tel_content.csv'
# ADELAIDE_CONTENT_FILE = 'adelaide_content.csv'

NEWS_AU_SOURCE = "news.com.au"
# DAILY_TEL_SOURCE = "dailytelegraph"
# ADELAIDE_SOURCE = "adelaidenow.com.au"


def sample():
    URL_SAMPLE = "https://www.python.org"

    driver = webdriver.Chrome('chromedriver')
    driver.get(URL_SAMPLE)
    print(driver.title)
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.clear()
    search_bar.send_keys("getting started with python")
    search_bar.send_keys(Keys.RETURN)
    print(driver.current_url)

def search_news_au():

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)

    URL_NEWS = "https://www.news.com.au/search-results?q=building+defect"
    driver.get(URL_NEWS)

    #click sort by relevant
    try:
        search_sort =  driver.find_element(By.ID, 'searchSort')
        driver.implicitly_wait(30)
        select_element = search_sort.find_element(By.XPATH, './div/select')
        select = Select(select_element)
        select.select_by_visible_text('Sort By: Relevance')
    except Exception:
        print('Element not found')

    #Get all search links
    try:
        image_links = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "storyblock_image_link")))
    except TimeoutException:
        print("TimeoutException")
        driver.quit()

    news_au_site_urls = []
    adelaide_site_urls = []
    daily_tel_urls = []
    elements = driver.find_elements(By.CLASS_NAME,"storyblock_image_link")
    for el in elements:
        site_url = el.get_attribute('href')
        if NEWS_AU_SOURCE in site_url and "/video/" not in site_url:
            news_au_site_urls.append(site_url)
        # elif DAILY_TEL_SOURCE in site_url:
        #     daily_tel_urls.append(site_url)
        # elif ADELAIDE_SOURCE in site_url:
        #     adelaide_site_urls.append(site_url)
            
    columns = ['site_url']
    df_search_news_au = pd.DataFrame(news_au_site_urls, columns=columns)
    # df_search_daily_tel = pd.DataFrame(daily_tel_urls, columns=columns)
    # df_search_adelaide = pd.DataFrame(adelaide_site_urls, columns=columns)

    df_search_news_au.to_csv(NEWS_AU_SEARCH_FILE, index=False)
    # df_search_daily_tel.to_csv(DAILY_TEL_SEARCH_FILE, index=False)
    # df_search_adelaide.to_csv(ADELAIDE_SEARCH_FILE, index=False)

    driver.close()
    driver.quit()

def process_content():
    #<h1 id="story-headline">title</h1>
    #<div id="story-body"><p>body</p></div>
    # Get urls that we want to extract the content from
    df_site = pd.read_csv(NEWS_AU_SEARCH_FILE)
    site_urls = df_site['site_url']

    # get site urls
    # Get content    
    content_dicts = []
    for site_url in site_urls:
        page = requests.get(site_url)
        news_content = BeautifulSoup(page.content, "html.parser")

        # get title
        title = news_content.find("h1", id="story-headline").text
        print(title)

        # get published date
        published_date_el = news_content.find("meta", property="article:published_time")
        if published_date_el:
            published_date = published_date_el["content"][0:10]

        # No tags

        # get content in text
        story_body = news_content.find("div", id="story-body")
        news_elements = story_body.find_all("p")
        news_text = ""
        for news_el in news_elements:
            news_text = news_text + news_el.text + "\n\n"
        
        content_dict = [date.today(), NEWS_AU_SOURCE, site_url, published_date, title, news_text]
        content_dicts.append(content_dict)

    # save results to csv
    df_content = pd.DataFrame(content_dicts, columns=['created_date', 'source', 'site_url',	'published_date', 'title', 'content'])
    df_content.to_csv(NEWS_AU_CONTENT_FILE, header = True, index=False, encoding='utf-8-sig')   

def main():
    #search_news_au()
    process_content()
    #sample()
    print("Finish")

if __name__ == "__main__":
    main()


