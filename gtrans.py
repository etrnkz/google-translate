#Elphador 
#2015 E.C
import requests 
from bs4 import BeautifulSoup 


class Translator ( ):
        
    
    def translate (text, detect ="auto",dest ="en"):
        #encoding the text to url encoded format 
        text = requests.utils.quote(text)
        data = f"async=translate,sl:{detect},tl:{dest},st:{text},id:3646594465454,qc:true,ac:true,_id:tw-async-translate,_pms:qs,_fmt:pc"
        #pass Cookies in the resp statment for safest request
        resp = requests.post('https://www.google.com/async/translate',headers =headers,  data=data)
        clarify = BeautifulSoup (resp .text , "html.parser")
        detec_t = clarify.find("span" , id="tw-answ-detected-sl-name")
        detected = detec_t.text
        #Romanization works only for supported languages so it'll may retrieve None for rare languages     romanization = clarify.find("span" , id="tw-answ-source-romanization")
        b_romanz =  clarify.find("span", id= "tw-answ-romanization")  
        romanization = clarify.find("span", id="tw-answ-source-romanization")

   
        roman = romanization.text 
        b_roman = b_romanz.text
        result = clarify.find("span",id="tw-answ-target-text")
        last_op = result.text 
        print(f"{last_op} \ntranslated from {detected} to {dest}",f"Romanization \n {b_roman}{roman}")
        #Uncomment this  to see the whole request response 
        #print(clarify.prettify())
         
      
