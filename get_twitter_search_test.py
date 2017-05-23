from requests_oauthlib import OAuth1Session
import json
import sys
import random
import re

while True:
    search_words = input(u"words: ")

    C_KEY = "CaY2OcAHy3f06hJdZMq8n42Bf"
    C_SECRET = "3lxSo5CUy9LLF5ypB8fvBCO1Xx7yI8Q5eUCrL9y9EgwNe55hX6"
    A_KEY = "135038063-ylUKTTvJyjHnP5zsaNTVrvLMTKR16JXljkcLywb2"
    A_SECRET = "7eFJLXTv2Y0E8qN4Djo11xoW13sIIxvR7yIDdYV3g5jLz"


    def Search_words():
        url = "https://api.twitter.com/1.1/search/tweets.json?"
        params = {
            "q": search_words,
            "lang": "ja",
            "result_type": "recent",
            "count": "100"
        }
        tw = OAuth1Session(C_KEY, C_SECRET, A_KEY, A_SECRET)
        req = tw.get(url, params=params)
        tweets = json.loads(req.text)
        #print(tweets)
        for tweet in tweets["statuses"]:
            f = open("tweet.txt", "a", encoding='utf-8')
            lists = (tweet["text"])
            #lists = (tweet["text"].encode("utf-8"))
            print("**********")
            if "http" in lists:
                print(lists)
                lists = lists.split("http", 1)[0]
                lists = lists.split("@")[0]
                lists = lists.split("RT")[0]

                f.write(lists + "\n")
                f.flush()
                f.close()

    if search_words:
        Search_words()
    else:
        break