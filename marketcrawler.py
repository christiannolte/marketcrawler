import requests
from bs4 import BeautifulSoup
import signal
import time
import os
import sys

artikel=[]     

def get_url_content(url):
    return requests.get(url).text

def get_telegram_token():
    try:
        telegramToken=os.environ["telegramToken"]
        return(telegramToken)
    except:
        print("Problems reading environment variable 'telegramToken' maybe its not set")
        return("")


def get_telegram_channel():
    try:
        telegramChannel=os.environ["telegramChannel"]
        return(telegramChannel)
    except:
        print("Problems reading environment variable 'telegramChannel' maybe its not set")
        exit()

def get_dapnet():
    try:
        dapnet=os.environ["dapnet"]
    except:
        print("Problems reading environment variable 'dapnet' maybe its not set")
        exit()
    return(dapnet)
                                                                                 
                                                                                 
def send_dapnet(message):
    try:
        transmitterGroupName=os.environ["transmitterGroupName"]
    except:
        print("Problems reading environment variable 'transmitterGroupname' maybe its not set")
        exit()
    try:
        callsign=os.environ["callsign"]
    except:
        print("Problems reading environment variable 'callsign' maybe its not set")
        exit()
    try:
     dapneturl = 'http://www.hampager.de:8080/calls'
     headers = {'Content-type': 'application/json'}

     data = '{ "text": "'+message.replace("[","(").replace("]",")")+'", "callSignNames": ["'+callsign+'"], "transmitterGroupNames": ["'+transmitterGroupName+'"], "emergency": false }'
     data = data.encode('utf-8')
     response = requests.post(dapneturl, headers=headers, auth=(callsign, get_dapnet()), data=data)
     print(response)
    except:
     print("Dapnet did not work")
     post_via_telegram("Dapnet did not work "+environmentname)

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
   telegramurl = "https://api.telegram.org/bot"+get_telegram_token()+"/sendMessage?chat_id="+get_telegram_channel()+"&text="+meldung
   print(telegramurl)
   print(requests.get(telegramurl).json()) # this sends the message
  except:
   print("Telegram did not work")

def shutdown(signum, frame):
    print('Caught SIGTERM, shutting down')
    # Finish any outstanding requests, then...
    post_via_telegram("Bot auf "+environmentname+" wird beendet")
    exit(0)

 
print("Start of Marketcrawler")
signal.signal(signal.SIGTERM, shutdown)
errcnt=0
print("checking Environment variables")
blogurl="https://www.mikrocontroller.net/forum/markt"
try:
    print("checking telegramToken")
    os.environ["telegramToken"]
except:
    print("Problems reading environment variable 'telegramToken' maybe its not set")
    errcnt+=1

try:
    print("checking telegramChannel")
    os.environ["telegramChannel"]
except:
    print("Problems reading environment variable 'telegramChannel' maybe its not set")
    errcnt+=1

try:
    print("checking callsign")
    os.environ["callsign"]
except:
    print("Problems reading environment variable 'callsign' maybe its not set")
    errcnt+=1

try:
    print("checking dapnet")
    os.environ["dapnet"]
except:
    print("Problems reading environment variable 'dapnet' maybe its not set")
    errcnt+=1

try:
    print("checking envname")
    environmentname=os.environ["envname"]
except:
    print("Problems reading environment variable 'envname' maybe its not set")
    errcnt+=1

try:
    print("checking period")
    wartezeit=int(os.environ["period"])
except:
    print("Problems reading environment variable 'period' maybe its not set")
    errcnt+=1

try:
    print("checking errorwaittime")
    errorwaittime=int(os.environ["errorwaittime"])
except:
    print("Problems reading environment variable 'errorwaittime' maybe its not set")
    errcnt+=1

if errcnt>0:
    print("Environment not ok")
    exit(-1)


get_blog_content(blogurl)
neueste_artikel=get_blog_content(blogurl)
print("Bot wurde neu gestartet")
post_via_telegram("Bot wurde auf "+environmentname+" gestartet")
send_dapnet("Bot wurde auf "+environmentname+" gestartet")                                               
artikel=neueste_artikel
time.sleep(20)
while 1:
    try:                                                                         
      neueste_artikel=get_blog_content(blogurl)
    except:
      neueste_artikel=[]
      post_via_telegram("ZWANGSPAUSE ANFANG")
      time.sleep(errorwaittime)
      post_via_telegram("ZWANGSPAUSE ENDE")
    for ding in neueste_artikel:
        if ding in artikel:
            pass
            #print(ding+"---- gibt es schon")
        else:
            print(ding+"ist neu")
            #senden
            post_via_telegram("Neuer Eintrag im Markt: " + ding +" ("+environmentname+")")
            send_dapnet("Neuer Eintrag im Markt: " + ding +" ("+environmentname+")")
            artikel.append(ding)
    time.sleep(wartezeit)                          

