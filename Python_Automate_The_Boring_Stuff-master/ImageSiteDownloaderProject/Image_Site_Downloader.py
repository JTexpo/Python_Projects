import wget
import urllib

def getAllComics():
    page = 1
    comicList = []
    head = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    while True:
        link = 'http://pusheen.com/category/comics/page/{}'.format(page)
        try:
            req = urllib.request.Request(url = link, headers = head)
            pageSource = str(urllib.request.urlopen(req).read()).split()
        except:
            print("All done! pages found were: {}".format(page))
            return comicList
        
        for i in pageSource:
            if ('pusheen.com/wp-content/uploads' in i) and ('gif' in i):
                if not( (i[i.index("https"):i.index('gif')+3]) in comicList):
                    comicList.append(i[i.index("https"):i.index('gif')+3])
        page += 1

def downloadComics(comics):
    comicNumber = 0
    head = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    for i in comics:
        f = open('{}.gif'.format(comicNumber),'wb')
        req = urllib.request.Request(url = i, headers = head)
        f.write(urllib.request.urlopen(req).read())
        f.close()
        comicNumber += 1
        
if __name__ == "__main__":
    myList = getAllComics()
    downloadComics(myList)
