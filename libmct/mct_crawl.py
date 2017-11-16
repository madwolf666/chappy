# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1Session

# 天気予報取得
def Crawl_Get_Weather(h_payload):
    """
    :param h_payload:   例）{'city':'130010'}
    :return:            天気予報
    """

    #id一覧：http://weather.livedoor.com/forecast/rss/primary_area.xml
    #payload = { 'city': '130010' }
    #print(h_payload)
    a_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    a_weather_data = requests.get(a_url, params=h_payload).json()
    #print(a_weather_data)
    #print(a_weather_data.keys())

    a_result = ""
    for a_weather in a_weather_data['forecasts']:
        '''
        print(
            a_weather['dateLabel']
            + 'の天気は'
            + a_weather['telop']
        )
        '''
        a_result += a_weather['dateLabel'] + 'の天気は' + a_weather['telop'] + "\n"

    return a_result

# Wikiデータ取得
def Crawl_Find_MediaWiki(h_title, h_outFile):
    """
    :param h_title:     検索タイトル
    :param h_outFile:   検索結果出力ファイル名
    :return:            検索結果（タイトルのみ）
    """
    #MediaWiki-API：https://www.mediawiki.org/w/api.php

    #MediaWikiのAPIにアクセスするためのURL
    a_url = 'https://ja.wikipedia.org/w/api.php'
    #カテゴリ一覧を取得するためのクエリ情報
    a_api_params1 = {
        'action': 'query',
        'titles': h_title,
        'prop': 'categories',
        'format': 'json'
    }
    #検索キーワードにマッチしたページのデータをHTML形式で取得するためのクエリ情報
    a_api_params2 = {
        'action': 'query',
        'titles': h_title,
        'prop': 'revisions',
        'rvprop': 'content',
        'format': 'xmlfm'
    }
    a_categories = requests.get(a_url, params=a_api_params1).json()
    a_json_dump = json.dumps(a_categories, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    #print(a_json_dump)
    a_page_id = a_categories['query']['pages']
    a_result = ""
    a_isOK = True

    if '-1' in a_page_id:
        a_result = '該当するページがありません'
        #print(a_result)
        a_isOK = False

    else:
        a_id = list(a_page_id.keys())
        if 'categories' in a_categories['query']['pages'][a_id[0]]:
            a_categories = a_categories['query']['pages'][a_id[0]]['categories']
            #for t in a_categories:
                #print(t['title'])
        else:
            a_result = '保存できるページを検索できませんでした'
            #print(a_result)
            a_isOK = False

    if (a_isOK == True):
        if (h_outFile != ""):
            a_data = requests.get(a_url, params=a_api_params2)
            #    json_dump = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            #print(a_data)
            with open(h_title + '.html', 'w', encoding='utf_8') as a_f:
                a_f.write(a_data.text)

    return a_result

# RSS取得
def Crawl_Get_Rss(h_site_name, h_url, h_outFile):
    """
    :param h_site_name:     サイト名
    :param h_url:           RSSのURL
    :param h_outFile:       取得結果出力フィル名
    :return:                取得結果
    """
    a_xml = requests.get(h_url)
    a_xml.encoding=a_xml.apparent_encoding
    a_soup = BeautifulSoup(a_xml.text, 'html.parser')
    #print(a_soup)
    a_result = ''

    a_result += '********************************************************************************\n'
    a_result += '*** ' + h_site_name + ' ***\n'
    a_result += '********************************************************************************\n'

    for news in a_soup.findAll('item'):
        #print(news)
        #print(news.title.string, news.link.string)
        #Python2
        #a_result += '■' + news.title.string.encode('utf-8') + '\n'
        #if (news.link != None):
        #    a_result += str(news.link.string).encode('utf-8') + '\n'
        #elif (news.guid != None):
        #    a_result += str(news.guid.string).encode('utf-8') + '\n'
        #Python3
        a_result += '■' + news.title.string + '\n'
        a_result += news.link.string + '\n'
        # print(a_result)

    if (h_outFile != ""):
        a_f = open(h_outFile, "w", 'utf-8')
        #a_f = open(h_outFile, "w", encoding='utf-8')
        a_f.write(a_result)
        a_f.flush()
        a_f.close()

    return a_result

# twitter検索
def Crawl_Find_Twitter(h_auth, h_words, h_outFile):
    """
    :param h_auth:      以下の形式
        {
        "C_KEY": "CaY2OcAHy3f06hJdZMq8n42Bf",
        "C_SECRET":"3lxSo5CUy9LLF5ypB8fvBCO1Xx7yI8Q5eUCrL9y9EgwNe55hX6";
        "A_KEY":"135038063-ylUKTTvJyjHnP5zsaNTVrvLMTKR16JXljkcLywb2";
        "A_SECRET":"7eFJLXTv2Y0E8qN4Djo11xoW13sIIxvR7yIDdYV3g5jLz"
        }
    :param h_words:     検索文字
    :param h_outFile:   検索結果出力フィル名
    :return:            検索結果
    """

    a_url = "https://api.twitter.com/1.1/search/tweets.json?"
    a_params = {
        "q": h_words,
        "lang": "ja",
        "result_type": "recent",
        "count": "100"
    }
    a_tw = OAuth1Session(h_auth["C_KEY"], h_auth["C_SECRET"], h_auth["A_KEY"], h_auth["A_SECRET"])
    a_req = a_tw.get(a_url, params=a_params)
    a_tweets = json.loads(a_req.text)
    #print(json.dumps(a_tweets, indent=4, separators=(',', ': ')))

    a_result = ""

    for a_tweet in a_tweets["statuses"]:
        a_lists = (a_tweet["text"])
        #lists = (tweet["text"].encode("utf-8"))
        #print("**********")
        if "http" in a_lists:
            #print(lists)
            a_lists = a_lists.split("http", 1)[0]
            a_lists = a_lists.split("@")[0]
            a_lists = a_lists.split("RT")[0]
            a_result += a_lists + "\n"

    if (h_outFile != ""):
        a_f = open(h_outFile, "w", encoding='utf-8')
        a_f.write(a_result)
        a_f.flush()
        a_f.close()

    return a_result
