from __future__ import print_function
import time
import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint
from aylienapiclient import textapi

configuration = aylien_news_api.Configuration()
configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'b3469cae'
configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '0dbc2a5397d70d63394d64904823ce3a'
configuration.host = "https://api.aylien.com/news/stories"

client = aylien_news_api.ApiClient(configuration)
api_instance = aylien_news_api.DefaultApi(client)

try:
    api_response = api_instance.list_stories(
        text='Building defect',
        published_at_start='NOW-30DAYS',
        published_at_end='NOW',
        source_locations_country=['AU']
    )
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %s\n" % e)

stories = api_response['stories']
if len(stories) > 0:
    print(stories[0]['title'])
    print(stories[0]['links']['permalink'])

def text_analysis():
    client = textapi.Client("b3469cae", "0dbc2a5397d70d63394d64904823ce3a")
    sentiment = client.Sentiment({'text': 'John is a very good football player!'})
    #aylienapiclient.errors.HttpError: <HttpError 403 when requesting https://api.aylien.com/api/v1/sentiment returned "b'Authentication failed'">
