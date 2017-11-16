# -*- coding: utf-8 -*-

import sys
import libmct.mct_crawl as mct_crawl
import libmct.mct_mail as mct_mail
#from libmct import mct_crawl
#from libmct import mct_mail

if __name__ == '__main__':
    args = sys.argv

    #Yahoo
    a_result = mct_crawl.Crawl_Get_Rss('Yahoo', 'http://news.yahoo.co.jp/pickup/science/rss.xml', '')
    #a_result = mct_crawl.Crawl_Get_Rss('Yahoo', 'http://news.yahoo.co.jp/pickup/science/rss.xml', "yahoo.txt")
    #CNET Japan
    a_result += mct_crawl.Crawl_Get_Rss('CNET Japan', 'http://feeds.japan.cnet.com/rss/cnet/all.rdf', '')
    #a_result += mct_crawl.Crawl_Get_Rss('CNET Japan', 'http://feeds.japan.cnet.com/rss/cnet/all.rdf', "cnet.txt")
    #Impress Watch HeadLine
    a_result += mct_crawl.Crawl_Get_Rss('Impress Watch Headline', 'http://rss.rssad.jp/rss/headline/headline.rdf', '')
    #a_result += mct_crawl.Crawl_Get_Rss('Impress Watch Headline', 'http://rss.rssad.jp/rss/headline/headline.rdf', "impress.txt")
    #IT Media
    a_result += mct_crawl.Crawl_Get_Rss('IT Media', 'http://rss.rssad.jp/rss/itmnews/2.0/news_bursts.xml', '')
    #a_result += mct_crawl.Crawl_Get_Rss('IT Media', 'http://rss.rssad.jp/rss/itmnews/2.0/news_bursts.xml', "itmedia.txt")
    #ZDNet Japan
    a_result += mct_crawl.Crawl_Get_Rss('ZDNet Japan', 'http://feeds.japan.zdnet.com/rss/zdnet/all.rdf', '')
    #a_result += mct_crawl.Crawl_Get_Rss('ZDNet Japan', 'http://feeds.japan.zdnet.com/rss/zdnet/all.rdf', "zdnet.txt")

    #Engadget Japanese
    a_result += mct_crawl.Crawl_Get_Rss('Engadget Japanese', 'http://japanese.engadget.com/rss.xml', '')
    #a_result += mct_crawl.Crawl_Get_Rss('Engadget Japanese', 'http://japanese.engadget.com/rss.xml', "engadget.txt")
    #Gizmodo Japan
    a_result += mct_crawl.Crawl_Get_Rss('Gizmodo Japan', 'http://www.gizmodo.jp/index.xml', '')
    #a_result += mct_crawl.Crawl_Get_Rss('Gizmodo Japan', 'http://www.gizmodo.jp/index.xml', "gizmob.txt")
    #ガジェット通信
    a_result += mct_crawl.Crawl_Get_Rss('ガジェット通信', 'http://getnews.jp/feed', '')
    #a_result += mct_crawl.Crawl_Get_Rss('ガジェット通信', 'http://getnews.jp/feed', "gadget.txt")

    #ライフハッカー
    a_result += mct_crawl.Crawl_Get_Rss('ライフハッカー', 'http://www.lifehacker.jp/index.xml', '')
    #a_result += mct_crawl.Crawl_Get_Rss('ライフハッカー', 'http://www.lifehacker.jp/index.xml', "lifehacker.txt")
    #GIGAZINE
    a_result += mct_crawl.Crawl_Get_Rss('GIGAZINE', 'http://feed.rssad.jp/rss/gigazine/rss_2.0', '')
    #a_result += mct_crawl.Crawl_Get_Rss('GIGAZINE', 'http://feed.rssad.jp/rss/gigazine/rss_2.0', "gigazine.txt")

    #print(a_result)

    #JP='iso-2022-jp'
    auth = {
        "IS_SSL":True,
        "SMTP":"",
        "SMTP_SSL":"smtp.gmail.com",
        "PORT":465,
        "LOGIN_MAIL":args[1],
        "LOGIN_PASS":args[2],
    }

    msg = {
        "SUBJECT":"Today\'s RSS",
        "FROM":args[1],
        "TO":args[3],
        "BODY":a_result
    }

    mct_mail.Mail_Send(auth, msg)
