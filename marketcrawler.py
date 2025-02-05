import requests
from bs4 import BeautifulSoup
import time
import os

artikel=[]                                                                       

# gibt html code der gewünschten url zurück
def get_url_content(url):
    return requests.get(url).text

def get_telegram_token():
    try:
        telegramToken=os.environ["telegramToken"]
        return(telegramToken)
    except:
        print("Problems reading environment variable 'telegramToken' maybe its not set")
        os.exit()


def get_telegram_channel():
    try:
        telegramChannel=os.environ["telegramChannel"]
        return(telegramChannel)
    except:
        print("Problems reading environment variable 'telegramChannel' maybe its not set")
        os.exit()

def get_dapnet():
    try:
        dapnet=os.environ["dapnet"]
    except:
        print("Problems reading environment variable 'dapnet' maybe its not set")
        os.exit()
    return(dapnet)
                                                                                 
                                                                                 
def send_dapnet(message):
    try:
        transmitterGroupName=os.environ["transmitterGroupName"]
    except:
        print("Problems reading environment variable 'transmitterGroupname' maybe its not set")
        os.exit()
    try:
        callsign=os.environ["callsign"]
    except:
        print("Problems reading environment variable 'callsign' maybe its not set")
        os.exit()
    try:
     dapneturl = 'http://www.hampager.de:8080/calls'
     headers = {'Content-type': 'application/json'}

     data = '{ "text": "'+message.replace("[","(").replace("]",")")+'", "callSignNames": ["'+callsign+'"], "transmitterGroupNames": ["'+transmitterGroupName+'"], "emergency": false }'
     data = data.encode('utf-8')
     response = requests.post(dapneturl, headers=headers, auth=(callsign, get_dapnet()), data=data)
     print(response)
    except:
     print("Dapnet did not work")
     post_via_telegram("Dapnet did not work")

def get_blog_content(url):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Neuer Durchlauf "+str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min))
    content = get_url_content(url)                                               
    # übergebe html an beautifulsoup parser
    subjects=[]
    soup = BeautifulSoup(content, "html.parser")
    for post in soup.findAll('td', {'class': 'subject'}):                        
        #print(post)
        #print("-------")
        #print(post.find('a').text)
        subjects.append(post.find('a').text)
    return(subjects)


def post_via_telegram(meldung):
  try:
   telegramurl = "https://api.telegram.org/bot"+get_telegram_token()+"/sendMessage?chat_ilsd="+get_telegram_channel()+"&text="+meldung
   print(requests.get(telegramurl).json()) # this sends the message
  except:
   print("Telegram did not work")

 
print(os.getcwd())
print(os.listdir())
try:
    blogurl=os.environ["blogurl"]
except:
    print("Problems reading environment variable 'blogurl' maybe its not set")
    os.exit()
get_blog_content(blogurl)
neueste_artikel=get_blog_content(blogurl)
print("Bot wurde neu gestartet")
post_via_telegram("Bot wurde gestartet")
send_dapnet("Bot wurde gestartet")                                               
artikel=neueste_artikel
time.sleep(20)
while 1:
    try:                                                                         
      neueste_artikel=get_blog_content(blogurl)
    except:
      neueste_artikel=[]
      post_via_telegram("ZWANGSPAUSE ANFANG")
      time.sleep(900)
      post_via_telegram("ZWANGSPAUSE ENDE")
    for ding in neueste_artikel:
        if ding in artikel:
            pass
            #print(ding+"---- gibt es schon")
        else:
            print(ding+"ist neu")
            #senden
            post_via_telegram("Neuer Eintrag im Markt: " + ding)
            send_dapnet("Neuer Eintrag im Markt: " + ding)
            artikel.append(ding)
    time.sleep(300)                          

