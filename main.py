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


@app.get("/generate-qr-code")
def generate(message: str,short: bool = 1):
    if re.match("^http(s|):\/\/.+\..+",message):
        try:
            if short == 1:
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
    else:
        return {"error":"please ensure a URL is parsed"}



