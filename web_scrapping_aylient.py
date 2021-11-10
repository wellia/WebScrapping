import os
import requests
import datetime
from dateutil.tz import tzutc
import json
import time
import pandas as pd
import numpy as np
import math
from tqdm import tqdm
from pprint import pprint
import codecs

headers = {
    'X-AYLIEN-NewsAPI-Application-ID': 'b3469cae', 
    'X-AYLIEN-NewsAPI-Application-Key': '0dbc2a5397d70d63394d64904823ce3a'
}

# https://docs.aylien.com/newsapi/search-taxonomies/#search-labels-for-iab-qag
category_ids = {'newsmedia': '01026002',
                'newspaper': '01026003',
                'construction_property': '04004000',
                'house_building': '04004002',
                'newsagency': '04010004',
                'newspaper_magazine': '04010005',
                'online': '04010006',
                'report': '17003000',
                'statistic': '17004000'}


def print_keyword_mention(story, element_x, keyword_x):
    body_x = story[element_x].lower()
    keyword_x = keyword_x.lower()
    # extract a window around key entity
    e_idx = body_x.find(keyword_x)
    e_end = e_idx + len(keyword_x)
    if e_idx >= 0:
        print('found ', e_idx)
        e_str = body_x[e_idx-100:e_idx] + "\033[1m" + body_x[e_idx:e_end] + "\033[0m " + body_x[e_end+1:e_end+51]
        print(f'{e_str}')
        
    elif element_x == 'title':
        print(story['title'])

def get_stories(params, print_params = None, print_count = None, print_story = None):
    print('get_stories')
    if print_params is None or print_params == 'yes':
        pprint(params)
    
    fetched_stories = []
    stories = None
    while stories is None or len(stories) > 0:
        try:
            response = requests.get('https://api.aylien.com/news/stories', params=params, headers=headers).json()
        except Exception as e:
            print(e)
            continue
            
        if 'errors' in response or 'error' in response:
            pprint(response)
        
        stories = response['stories']
        
        params['cursor'] = response['next_page_cursor']
        
        fetched_stories += stories
        
    return fetched_stories

def save_to_df(stories):
    # create dataframe in the format we want
    cols = ['id', 'title', 'permalink', 'published_at', 'source', 'summary', 'keywords', 'categories', 'clusters', 'body']
    df = []
    titles = []
    for story in stories:
        # make array of the fields we're interested in
        sentences = story['summary']['sentences']
        summary_text = '\n\n'.join(sentences)
        if len(summary_text) > 0:
            data = [
                story['id']
                , story['title']
                , story['links']['permalink']
                , story['published_at']
                , story['source']['domain']
                , summary_text
                , story['keywords']
                , story['categories']
                , story['clusters']
                , story['body']]
        
        zipped = zip(cols, data)
        a_dictionary = dict(zipped)
        title = a_dictionary.get("title")
        if title not in titles:
            titles.append(title)
            df.append(a_dictionary)
    
    df = pd.DataFrame(df, columns = cols)

    df.to_csv('test_aylient.csv', index=False)

    print("saved %s stories" %(len(df)))

def save_to_json(stories):
    with open('data.json', 'w') as f:
        json.dump(stories, f)

    file = codecs.open("data2.json", "w", "utf-8")
    for story in stories:
        file.write(story.text)
        file.write("\n")
        file.close()

# aql inventories
#((defect leak peel damp deterioration deform faulty break crumble safety dodgy) AND \
#(door build apartment unit roof door construction electric structural floor wall high-rise house waterproof)) OR \
                
def main():
    
  # define the query parameters
    params = {
        'language[]': ['en'],
        'aql':  'body:("building defect"^10 OR \
                    "build defect"~5 OR \
                    "structural problem"~5 OR \
                    "water damage"~5 OR \
                    "buckled window"~5 OR \
                    "cladding"^10 OR "waterproofing problem" OR "drainage" OR \
                    "structural damage"~5 OR \
                    "fire safety"~5 OR \
                    "door cavities"~5 OR \
                    "foundation damage"~5 OR \
                    "peel paint"~5 OR \
                    "peel wall"~5 OR \
                    "crack wall"~5 OR \
                    "crack floor"~5 OR \
                    "electrical defect"~5 OR \
                    "foundation problem"~5)',
        'published_at.start':'NOW-2MONTHS',
        'published_at.end':'NOW',
        'cursor': '*',
        'per_page' : 50,
        'source.locations.country[]' : ['AU'],
        'categories.taxonomy[]': 'iptc-subjectcode',
        'categories.id[]': [category_ids['construction_property'],
                            category_ids['house_building'],
                            category_ids['newsagency'],
                            category_ids['newsmedia'],
                            category_ids['newspaper'],
                            category_ids['newspaper_magazine'],
                            category_ids['online'],
                            category_ids['report'],
                            category_ids['statistic']],
        'sort_by' : 'relevance'
    }

    stories = get_stories(params)

    keywords = ["Build", "defect"]

    #save_to_df(stories)

    save_to_json(stories)

    print('************')
    print("Fetched %s stories" %(len(stories)))

        
if __name__ == "__main__":
    main()

