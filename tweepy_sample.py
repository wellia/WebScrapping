import tweepy
import json
import pandas as pd

# Authenticate to Twitter
CONSUMER_KEY = "PIqzhDQNxpJ55YVeRjQaGVyjz"
CONSUMER_SECRET = "MDs2RjQwELGJ2Vw9ti6yyeRko3e6YLvIfijlXfJ4hNRTh2jLkz"
ACCESS_TOKEN = "1457889815907561475-7kn7FbG3OjBzlts6d0H2N4LZbJaZiA"
ACCESS_TOKEN_SECRET = "NWfUpwieVYE99UjRIrjdTabIR0ifj7veQDzMraOtgar8y"
QUERY = "'building defect' OR 'apartment defect' OR (%23building and defect)"
FILE_NAME = 'tweepy_sample.json'
CSV_FILE = 'tweepy_sample.csv'

def connect_twitter(api):
    success = False
    # test authentication
    try:
        api.verify_credentials()
        print("Authentication OK")
        success = True
    except:
        print("Error during authentication")
    return success

def save_to_df(json_response):
    # create dataframe in the format we want
    cols = ['created_at','text']
    df = []
    statuses = json_response['statuses']
    for status in statuses:
        data = [status['created_at'], status['text']]    
        zipped = zip(cols, data)
        a_dictionary = dict(zipped)
        df.append(a_dictionary)
    
    df = pd.DataFrame(df, columns = cols)

    df.to_csv(CSV_FILE, index=False)

    print("saved %s twits" %(len(df)))

def main():

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    if connect_twitter(api):
        json_response = api.search_tweets(q=QUERY, lang="en", parser=tweepy.parsers.JSONParser())
        
        #print(json.dumps(json_response, indent=4, sort_keys=True))

        # with open(FILE_NAME, 'w', encoding='utf-8') as f:
        #     json.dump(json_response, f, ensure_ascii=False, indent=4)

        save_to_df(json_response)
        
if __name__ == "__main__":
    main()
