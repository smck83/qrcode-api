# qrcode-api
 An API built using fastAPI that returns a dynamic QR code pointing to a URL in the GET variable `message`

 e.g. 
 `https://localhost:8000/generate-qr-code?message=https://example.com`

Similiar qrcode GET API here (which is a modified fork of a project that requires a POST) and can be hosted as a Cloudflare Worker (free)
https://github.com/smck83/qrcode-cloudflare-worker

 ## URL shortnening
 Support for URL shortener service `short.io` has been added. This allows you to keep the QR code version low, which means a more simple QR code.

 TO use `https://short.io` you will need to signup for a FREE or PAID account and parse the two(2) `ENVIRONMENT VARIABLES` to the docker container:

 - `SHORTIO_APIKEY`
 - `SHORTIO_DOMAIN`

 ## How to run
To run the container:
````
docker run -it -p 8000:8000 smck83/qrcode-api
````

To run the container, with short.io integration:

````
 docker run -it -p 8000:8000 -e SHORTIO_APIKEY="<--  Your short.io API key-->" -e SHORTIO_DOMAIN="<-- Your short.io Domain Name -->" smck83/qrcode-api
````

It is also possible to restrict the hostnames allowed by the API in the message=. e.g. to lockdown to Mimecast Awareness Training Phishing Simulation URLs:

````
 docker run -it -p 8000:8000 -e EXPAND_HOSTNAMES="True" -e ALLOWED_HOSTNAMES="therelayservice.com" smck83/qrcode-api
````

| ENV VARIABLES|  Required? | Description |
| ------------- | ------------- | ------------- |
| ALLOWED_HOSTNAMES | No | Default `*` : restrict the API to a space seperated list of authorized hostnames |
| EXPAND_HOSTNAMES | No | Default `False` : When set to `True` top level hostnames will be included from `ALLOWED_HOSTNAMES`, e.g. When `True` and `/?message=https://host3.host2.host1.com/abc123` - script will check `ALLOWED_HOSTNAMES` for `host3.host2.host1.com` AND also TLD, `host1.com` instead of only host3.host2.host1.com|
| SHORTIO_APIKEY | No | Default `None` :  https://short.io API Key if you wish to use URL shortening |
| SHORTIO_DOMAIN | No | Default `None` :  https://short.io Domain Name to create short URLs. Dependant on `SHORTIO_APIKEY` |
