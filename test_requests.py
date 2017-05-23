import mct_crawl

if __name__ == '__main__':
    a_payload = {'city':'016010'}
    a_result= mct_crawl.Crawl_Get_Weather(a_payload)
    print("*** 札幌の天気予報 ***")
    print(a_result)

    a_title = input('何を検索しますか? >')
    a_result = mct_crawl.Crawl_Find_MediaWiki(a_title, "mediawiki.txt")
