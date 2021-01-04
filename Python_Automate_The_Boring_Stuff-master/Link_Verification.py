import wget
import urllib
        
if __name__ == "__main__":
    head = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    link = str(input("What Is The Website You Wish To Visit : "))
    if not link.startswith('https://'):
        link = 'https://' + link 
    try:
        req = urllib.request.Request(url = link, headers = head)  
        pageSource = str(urllib.request.urlopen(req).read()).split()
        print("This Website Is Real")
    except:
        print("This Website Is Not Real")
    
