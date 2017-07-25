import mct_crawl
import mct_mail

if __name__ == '__main__':
    #Yahoo
    a_result = mct_crawl.Crawl_Get_Rss('Yahoo', 'http://news.yahoo.co.jp/pickup/science/rss.xml', "yahoo.txt")
    #CNET Japan
    a_result += mct_crawl.Crawl_Get_Rss('CNET Japan', 'http://feeds.japan.cnet.com/rss/cnet/all.rdf', "cnet.txt")
    #Impress Watch HeadLine
    a_result += mct_crawl.Crawl_Get_Rss('Impress Watch Headline', 'http://rss.rssad.jp/rss/headline/headline.rdf', "impress.txt")
    #IT Media
    a_result += mct_crawl.Crawl_Get_Rss('IT Media', 'http://rss.rssad.jp/rss/itmnews/2.0/news_bursts.xml', "itmedia.txt")
    #ZDNet Japan
    a_result += mct_crawl.Crawl_Get_Rss('ZDNet Japan', 'http://feeds.japan.zdnet.com/rss/zdnet/all.rdf', "zdnet.txt")

    #Engadget Japanese
    a_result += mct_crawl.Crawl_Get_Rss('Engadget Japanese', 'http://japanese.engadget.com/rss.xml', "engadget.txt")
    #Gizmodo Japan
    a_result += mct_crawl.Crawl_Get_Rss('Gizmodo Japan', 'http://www.gizmodo.jp/index.xml', "gizmob.txt")
    #ガジェット通信
    a_result += mct_crawl.Crawl_Get_Rss('ガジェット通信', 'http://getnews.jp/feed', "gadget.txt")

    #ライフハッカー
    a_result += mct_crawl.Crawl_Get_Rss('ライフハッカー', 'http://www.lifehacker.jp/index.xml', "lifehacker.txt")
    #GIGAZINE
    a_result += mct_crawl.Crawl_Get_Rss('GIGAZINE', 'http://feed.rssad.jp/rss/gigazine/rss_2.0', "gigazine.txt")

    #print(a_result)

    #JP='iso-2022-jp'
    auth = {
        "IS_SSL":True,
        "SMTP":"",
        "SMTP_SSL":"smtp.gmail.com",
        "PORT":465,
        "LOGIN_MAIL":"",
        "LOGIN_PASS":"",
    }

    msg = {
        "SUBJECT":"Today\'s RSS",
        "FROM":"",
        "TO":"",
        "BODY":a_result
    }

    mct_mail.Mail_Send(auth, msg)
