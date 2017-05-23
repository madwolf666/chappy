import sys
#from natto import MeCab
import MeCab
import random
import re
import mct_crawl
import mct_scrap
import mct_mail

while True:
    search_words = input(u"words: ")

    twitter_auth = {
        "C_KEY":"CaY2OcAHy3f06hJdZMq8n42Bf",
        "C_SECRET":"3lxSo5CUy9LLF5ypB8fvBCO1Xx7yI8Q5eUCrL9y9EgwNe55hX6",
        "A_KEY":"135038063-ylUKTTvJyjHnP5zsaNTVrvLMTKR16JXljkcLywb2",
        "A_SECRET":"7eFJLXTv2Y0E8qN4Djo11xoW13sIIxvR7yIDdYV3g5jLz"
    }

    def Search_words():
        a_result = mct_crawl.Crawl_Find_Twitter(twitter_auth, search_words, "tweet.txt")
        return a_result

    def Mecab_file():
        wordlist = mct_scrap.Scrap_Mecab_Wakati("", "tweet.txt","wakati.txt")
        #print("wordlist\n")
        #print(wordlist)
        dict = mct_scrap.Scrap_Mecab_Markov_Dict(wordlist, "")
        #print(dict)
        sus = mct_scrap.Scrap_Mecab_Markov_Chain(wordlist, dict, 90, "[!-/:-@[-`{-~]")

        words = re.sub(re.compile("[!-~]"), "", sus)
        twits = words + " 【tweet from chappy】"
        #print(twits)

        #url = "https://api.twitter.com/1.1/statuses/update.json"
        #params = {"status": twits, "lang": "ja"}
        #tw = OAuth1Session(C_KEY, C_SECRET, A_KEY, A_SECRET)
        #req = tw.post(url, params=params)
        #if req.status_code == 200:
        #    print
        #    "Success! Your Tweet"
        #else:
        #    print
        #    req.status_code
        return twits

    def Janome_file():
        wordlist = mct_scrap.Scrap_Janome_Parse("", "tweet.txt","janome_parse.txt")
        #print("wordlist\n")
        #print(wordlist)
        dict = mct_scrap.Scrap_Janome_Markov_Dict(wordlist, "")
        print(dict)
        sus = mct_scrap.Scrap_Janome_Markov_Chain(wordlist, dict)
        print(sus)
        sus = mct_scrap.Scrap_Janome_Markov_Overlap(sus)
        print(sus)

        twits = sus + "\n 【tweet from chappy】"
        return twits

    if search_words:
        mail_auth = {
            "IS_SSL":True,
            "SMTP":"",
            "SMTP_SSL":"smtp.gmail.com",
            "PORT":465,
            "LOGIN_MAIL":"madwolf699@gmail.com",
            "LOGIN_PASS":"chappy666",
        }

        a_result = Search_words()

        mail_msg = {
            "SUBJECT":"Today\'s Tweet Search",
            "FROM":"madwolf699@gmail.com",
            "TO":"madwolf666@live.jp",
            "BODY":a_result
        }

        #mct_mail.Mail_Send(mail_auth, mail_msg)

        #twits = Mecab_file()
        twits = Janome_file()

        mail_msg = {
            "SUBJECT":"Today\'s Tweet Merkov",
            "FROM":"madwolf699@gmail.com",
            "TO":"madwolf666@live.jp",
            "BODY":twits
        }

        mct_mail.Mail_Send(mail_auth, mail_msg)

    else:
        break