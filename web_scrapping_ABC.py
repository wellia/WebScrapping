#-----------------------------------------------------
# codes to scrap building defect news contents 
#-----------------------------------------------------

# https://www.lookupstrata.com.au/

#pip install requests_html
#pip install requests
#pip install BeautifulSoup

import requests
import pandas as pd
from requests_html import HTMLSession
from datetime import date
from bs4 import BeautifulSoup

# Declare constants
source_ABC = 'ABC'
source_NEWDAILY = 'NewDaily'
abc_search_base_url = 'https://search-beta.abc.net.au/index.html?siteTitle=news#/?query=building%20defect&configure%5BgetRankingInfo%5D=true&configure%5BclickAnalytics%5D=true&configure%5BuserToken%5D=anonymous-54632831-5edd-4651-913b-d0445de8afbf&configure%5BhitsPerPage%5D=10&page='
news_search_base_url = 'https://www.news.com.au/search-results?q=building+defects'
new_daily_search_base_url = 'https://thenewdaily.com.au/?s=building+defect'
#https://thenewdaily.com.au/?paged=2&s=building+defect

#search_links = created_date, search_url, source, processed
search_file = 'search_links.csv'

#site_links = created_date, site_url, source, processed
site_file = 'site_links.csv'

#news_content = created_date, source, site_url, published_date, title, content, state
base_content_file = '_content.csv'

def construct_search_urls(search_base_url, source):
    search_urls = []

    for i in range(10):
        search_dict = [date.today(), source, search_base_url + str(i+1)]
        search_urls.append(search_dict)
    
    # save results to csv
    df = pd.DataFrame(search_urls)
    df.to_csv(search_file, mode='a', header=False, index=False)

def get_site_urls_from_search(search_urls, source):
    site_dicts = []

    # create an HTML Session object
    session = HTMLSession()
    
    # Use the object above to connect to needed webpage

    # search_urls2 = [search_urls[0], search_urls[1]]
    # print(search_urls2)
    i = 1
    for search_url in search_urls:
        print('process', i)
        i = i + 1
    
        resp = session.get(search_url)
        #print(resp)

        # Run JavaScript code on webpage
        resp.html.render()
        #print(resp.html.html)

        # process tags
        soup = BeautifulSoup(resp.html.html, "html.parser")
        #print(soup.prettify)

        if source == source_ABC:
            divs = soup.find_all("div", class_="card-layout__content--1j1us")
            for div in divs:
                for a in div.find_all('a', href=True):
                    #print("Found the URL:", a['href'])
                    site_dict = [date.today(), source, a['href']]
                    site_dicts.append(site_dict)

        if source == source_NEWDAILY:
            print('hi')
            #find article with class tnd-article-list__item and get the <a href='''>
    
    return site_dicts
 
def is_correct_news(html_content):
    search_tags1 = ["building", "buildings"]
    search_tags2 = ["defect", "defects"]
    search_tags=[search_tags1, search_tags2]

    tags = html_content.find_all("meta", property="article:tag")
    news_tags = set()
    for tag in tags:
        news_tags.add(tag["content"])
    print('News tags:',news_tags)

    is_correct_news = True
    for tags in search_tags:
        if not any(x in tags for x in news_tags):
            is_correct_news = False
            break
    
    print('right news?', is_correct_news)

    return is_correct_news


def get_news_content(site_urls, source):
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
        #print('News tags:',tag_string)

        # get content in text
        news_elements = news_content.find_all("p", class_="_1HzXw")
        news_text = ""
        for news_el in news_elements:
            news_text = news_text + news_el.text + "\n\n"
        
        content_dict = [date.today(), source, site_url, published_date, title, news_text, tag_string]
        content_dicts.append(content_dict)

    return content_dicts
        
def process_search_links(created_date, source):
    # Get urls on search result page
    df_search = pd.read_csv(search_file)
    search_urls = df_search[(df_search['source'] == source) & 
                    (df_search['created_date'] == created_date) &
                    (df_search['processed'] != 'y')]['search_url']

    # get site urls
    site_dicts = get_site_urls_from_search(search_urls, source)

    # save results to csv
    df_site = pd.DataFrame(site_dicts)
    df_site.to_csv(site_file, header = False, mode = 'a', index=False)

    # update search urls
    df_search['processed'] = 'y'
    df_search.to_csv(search_file, index=False)

def process_contents(created_date, source):
    # Get urls that we want to extract the content from
    df_site = pd.read_csv(site_file)
    site_urls = df_site[(df_site['source'] == source) & 
                    (df_site['created_date'] == created_date) &
                    (df_site['processed'] == 'y')]['site_url']

    # get site urls
    content_dicts = get_news_content(site_urls, source)

    # save results to csv
    content_file = source + base_content_file
    df_content = pd.DataFrame(content_dicts)
    df_content.to_csv(content_file, header = False, mode = 'a', index=False)

    # update search urls
    df_site['processed'] = 'y'
    df_site.to_csv(site_file, index=False)

def main():
    # Construct search links for each page
    #construct_search_urls(abc_search_base_url, source_ABC)

    created_date = '28/10/2021'
    source = source_ABC

    #process_search_links(created_date, source)

    process_contents(created_date, source)
        
def test():
    print("Hello World test!")

    

if __name__ == "__main__":
    main()