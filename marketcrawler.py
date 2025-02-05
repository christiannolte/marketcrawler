import requests                                                                  
from bs4 import BeautifulSoup                                                    
import time                                                                      
import os                                                                        
                                                                                 
artikel=[]                                                                       
                                                                                 
url = 'https://www.mikrocontroller.net/forum/markt'                              
                                                                                 
# gibt html code der gewünschten url zurück                                      
def get_url_content(url):                                                        
    return requests.get(url).text                                                
                                                                                 
def get_telegram_token():                                                        
     fd=open("./config/token.txt")                                               
     token=fd.read()                                                             
     fd.close()                                                                  
     return(token)                                                               
                                                                                 
def get_telegram_channel():                                                      
     fd=open("./config/channel.txt")
     channel=fd.read()

def get_dapnet():                                                                
     fd=open("./config/dapnet.txt")                                              
     dapnet=fd.read()                                                            
     fd.close()                                                                  
     return(dapnet)                                                              
                                                                                 
                                                                                 
def send_dapnet(message):                                                        
    try:                                                                         
     url = 'http://www.hampager.de:8080/calls'                                   
     headers = {'Content-type': 'application/json'}                              
     data = '{ "text": "'+message.replace("[","(").replace("]",")")+'", "callSignNames": ["dc4diy"], "transmitterGroupNames": ["dl-ni"], "emergency": false }'    
     data = data.encode('utf-8')                                                 
     response = requests.post(url, headers=headers, auth=('dc4diy', get_dapnet()), data=data)                                                                     
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
   url = "https://api.telegram.org/bot"+get_telegram_token()+"/sendMessage?chat_ils
   d="+get_telegram_channel()+"&text="+meldung                                      
   print(requests.get(url).json()) # this sends the message                      
  except:                                                                        
   print("Telegram did not work")                                                
                                                                                 
                                                                                 
print(os.getcwd())                                                               
print(os.listdir())                                                              
get_blog_content(url)                                                            
neueste_artikel=get_blog_content(url)                                            
print("Bot wurde neu gestartet")                                                 
post_via_telegram("Bot wurde gestartet")                                         
send_dapnet("Bot wurde gestartet")                                               
artikel=neueste_artikel                                                          
time.sleep(20)                                                                   
#send_message()                                                                  
while 1:                                                                         
    try:                                                                         
      neueste_artikel=get_blog_content(url)                                      
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
            post_via_telegram("Neuer Eintrag im Markt: "+ding)                   
            send_dapnet("Neuer Eintrag im Markt: "+ding)                         
            artikel.append(ding)                                                 
    time.sleep(300)                          

