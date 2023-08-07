import io
import qrcode
import json
from fastapi import FastAPI
from starlette.responses import StreamingResponse
import re
import requests
import os
from fastapi import FastAPI

cache = {}
shortenURLs = False

if 'SHORTIO_APIKEY' in os.environ:
    shortioKey = os.environ['SHORTIO_APIKEY']
    print("URL shortening is ON!")
    shortenURLs = True
if 'SHORTIO_DOMAIN' in os.environ:
    shortioDomain = os.environ['SHORTIO_DOMAIN']

if 'ALLOWED_HOSTNAMES' in os.environ:
    allowedHostnames = os.environ['ALLOWED_HOSTNAMES'].split(' ')
    print(allowedHostnames)
else:
    allowedHostnames =  []

def createShortIOURL(url):
    if shortenURLs == False:
        print ("URL Shortening is disabled")
        return url
    elif url not in cache:
        payload = {
            "allowDuplicates": False,
            "domain": shortioDomain,
            "originalURL": url
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            'authorization': shortioKey
        }
        response = requests.post("https://api.short.io/links", json=payload, headers=headers)
        output = json.loads(response.text)
        print(output)
        cache[url] = output["shortURL"]
        print(cache)
        #print(output["shortURL"])
        return output["shortURL"]
    elif url in cache:
        return cache[url]

app = FastAPI()

def genQRcode(message,short:bool = 1):
        try:
            if short == 1 and message != "[rawlink]":
                shortURL = createShortIOURL(message)
            else:
                print("URL Shortening override.")
                shortURL = message
        except Exception as e:
            print(e)
        else:
            img = qrcode.make(shortURL)
            buf = io.BytesIO()
            img.save(buf)
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/jpeg")


@app.get("/generate-qr-code")
def generate(message: str,short: bool = 1):
    if re.match("(^http(s|):\/\/.+\..+|\[rawlink\])",message):
        hostname = message
        if "/" in message and "." in message:
            explodeURL = message.split('/')
            hostname = explodeURL[2]
            hostname = hostname.split('.')
            hostname.reverse()
            hostname = hostname[1] + "." + hostname[0]
            print(hostname)
        if hostname in allowedHostnames or len(allowedHostnames) == 0:
            return genQRcode(message,short)
        elif message == "[rawlink]":
            return genQRcode(message,0)
        else:
            return {"error":"unauthorized"} 
    else:
        return {"error":"please ensure a URL is parsed"}



