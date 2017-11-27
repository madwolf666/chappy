#5.3　ディレクトリとファイルの総当たり攻撃

#import urllib2
import urllib
import urllib.error
import urllib.parse
import urllib.request
import threading
#import Queue
import queue

threads        = 5
target_url     = "http://testphp.vulnweb.com"
#wordlist_file  = "/tmp/all.txt" # from SVNDigger
wordlist_file = "C:\\Users\\hal\\PycharmProjects\\chappy\\dics\\SVNDigger\\all.txt"
resume         = None
user_agent     = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):

    # read in the word list
    #fd = open(wordlist_file,"rb")
    fd = open(wordlist_file,"r")
    raw_words = fd.readlines()
    fd.close()
    
    found_resume = False
    #words        = Queue.Queue()
    words        = queue.Queue()

    for word in raw_words:
        
        word = word.rstrip()

        if resume is not None:
            
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    #print "Resuming wordlist from: %s" % resume
                    print("Resuming wordlist from: %s" % resume)

        else:
            words.put(word)
    
    return words


def dir_bruter(extensions=None):
    
    while not word_queue.empty():
        attempt = word_queue.get()
        #print(attempt)
        attempt_list = []
        
        # check if there is a file extension if not
        # it's a directory path we're bruting
        if "." not in attempt:
        #if b"." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)
    
        # if we want to bruteforce extensions
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt,extension))
                
        # iterate over our list of attempts        
        for brute in attempt_list:
            
            #url = "%s%s" % (target_url, urllib.quote(brute))
            url = "%s%s" % (target_url, urllib.parse.quote(brute))
            #print(url)
            try:
                headers = {}
                headers["User-Agent"] = user_agent
                #r = urllib2.Request(url,headers=headers)
                r = urllib.request.Request(url,headers=headers)

                
                #response = urllib2.urlopen(r)
                response = urllib.request.urlopen(r)

                if len(response.read()):
                    #print "[%d] => %s" % (response.code,url)
                    print("[%d] => %s" % (response.code,url))

            #except urllib2.HTTPError,e:
            except urllib.error.HTTPError as error:

                #if e.code != 404:
                if error.code != 404:
                    #print "!!! %d => %s" % (e.code,url)
                    print("!!! %d => %s" % (error.code,url))

                pass


word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak",".orig",".inc"]

for i in range(threads):
            t = threading.Thread(target=dir_bruter,args=(extensions,))
            t.start()
