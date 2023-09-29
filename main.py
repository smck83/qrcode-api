import io
import qrcode
import json
from fastapi import FastAPI
from starlette.responses import StreamingResponse
import re
import requests
import os
from fastapi import FastAPI
import shortlink
from fastapi.responses import RedirectResponse

cache = {}
shortenURLs = False


if 'HOST_URL' in os.environ:
    host_url = os.environ['HOST_URL'] + "/g"
else:
    host_url = None

#host_url = "https://localhost:8000/g"

if 'SHORTIO_APIKEY' in os.environ:
    shortioKey = os.environ['SHORTIO_APIKEY']
    print("SHORTIO - URL shortening is ON!")
    shortenURLs = True
if 'SHORTIO_DOMAIN' in os.environ:
    shortioDomain = os.environ['SHORTIO_DOMAIN']

tldList = ['com','govt','org','edu','gov','co']

def getTLD(hostname):
    domain = hostname.split('.')
    domain.reverse()
    if len(domain) > 2 and domain[1] in tldList: # return three
        output =  f"{domain[2]}.{domain[1]}.{domain[0]}"
        #print(output)
        return output
    elif len(domain) > 1:
        output =  f"{domain[1]}.{domain[0]}"
        #print(output)
        return output
    else:
        return hostname

if 'ALLOWED_HOSTNAMES' in os.environ:
    allowedHostnames = (os.environ['ALLOWED_HOSTNAMES']).lower().split(' ')
    extraHostnames = []
    if 'EXPAND_HOSTNAMES' in os.environ and os.environ['EXPAND_HOSTNAMES'] == "True":
        print("EXPAND_HOSTNAME is True")
        for host in allowedHostnames:
            host = getTLD(host)
            extraHostnames.append(host)
    allowedHostnames = list(set(allowedHostnames + extraHostnames)) #remove duplicates
    print("Allowed Hostnames:",allowedHostnames)
else:
    allowedHostnames =  []
    print("Allowed Hostnames:","*")

def createShortIOURL(url):
    if shortenURLs == False:
        print ("SHORTIO - URL Shortening is disabled")
        if host_url != None:
            url = (createShortLink(url))['shortURL']
        return url
    elif url not in cache:
        payload = json.dumps({
            "allowDuplicates": False,
            "domain": shortioDomain,
            "originalURL": url
        })
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            'authorization': shortioKey
        }
        print(payload)
        response = requests.post("https://api.short.io/links", data=payload, headers=headers)
        output = json.loads(response.text)
        print("json payload:",output)
        cache[url] = output["shortURL"]
        print(cache)
        return output["shortURL"]
    elif url in cache:
        return cache[url]


def createShortLink(url: str,key = False,length:int = 5):
    outputURL = host_url + "/" + str(shortlink.createURL(url,key,length))
    output = { "shortURL": outputURL,
               "originalURL" : url
              }

    return output

app = FastAPI()

def genQRcode(message,short:bool = 1):
        try:
            if short == 1 and message != "[rawlink]":
                shortURL = createShortIOURL(message)
            else:
                print("URL Shortening override.")
                shortURL = (createShortLink(message))['shortURL']
                #shortURL = message
        except Exception as e:
            print(e)
        else:
            img = qrcode.make(shortURL)
            buf = io.BytesIO()
            img.save(buf)
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/jpeg")


@app.get("/generate-qr-code")
def generate(message,short: bool = 1):
    
    print("input message:",message)
    if re.match("(^http(s|):\/\/.+\..+|\[rawlink\])",message):
        hostname = ""
        tldHostname = ""
        if "/" in message and "." in message and message.lower() != "[rawlink]":
            explodeURL = message.split('/')
            hostname = explodeURL[2]
            
            print("Hostname:",hostname)
            if 'EXPAND_HOSTNAMES' in os.environ and os.environ['EXPAND_HOSTNAMES'] == "True":
                tldHostname = getTLD(hostname)
                print('TLD hostname:',tldHostname)
        if (tldHostname.lower() in allowedHostnames or hostname.lower() in allowedHostnames) or len(allowedHostnames) == 0:
            
            return genQRcode(message,short)
        elif message == "[rawlink]":
            return genQRcode(message,0) #don't send to URL shortener
        else:
            return {"error":"unauthorized"} 
    else:
        return {"error":"please ensure a URL is parsed"}

@app.get("/g/{key}", response_class=RedirectResponse, status_code=302)
async def redirect_short2Long(key):
    defaultRedirect = "https://github.com/smck83/qrcode-api"
    if key != None and shortlink.keyExists(key) == True:
        outputURL = shortlink.getURL(key)
        if "http" in outputURL:
            return outputURL
        else:
            return defaultRedirect
    else:
        return defaultRedirect



