# qrcode-api
 An API built using fastAPI that returns a dynamic QR code pointing to a URL in the GET variable `message`

 e.g. 
 
     https://localhost:8000/generate-qr-code?message=https://example.com

Similiar qrcode GET API here (which is a modified fork of a project that requires a POST) and can be hosted as a Cloudflare Worker (free)
https://github.com/smck83/qrcode-cloudflare-worker


NOTE: GET requests do not support special characters like # and &, as these are used for fragment identifier and parameters:
e.g.

    https://localhost:8000/generate-qr-code?message=https://example.com/?value=onetwothree&value2=threefourfive#abc123

To pass these variables successfuly, special characters such as # and & first be individually URL encoded:
e.g.

    https://localhost:8000/generate-qr-code?message=https://example.com/?value=onetwothree%26value2=threefourfive%23abc123

Where:
`& = %26`, and
`# = %23`


 ## URL shortnening

 ### Short.io

 Support for URL shortener service `short.io` has been added. This allows you to keep the QR code version low, which means a more simple QR code.

 TO use `https://short.io` you will need to signup for a FREE or PAID account and parse the two(2) `ENVIRONMENT VARIABLES` to the docker container:

 - `SHORTIO_APIKEY`
 - `SHORTIO_DOMAIN`

### Inbuilt URL shortener

https://github.com/smck83/shortlink-api has been added as an alternative. Shortlink is a builtin URL shortener. To enable this you only need to add an `ENVIRONMENT VARIABLE` at runtime called `HOST_URL`

NOTE: If SHORTIO_APIKEY environment variable is present, it will take precedence over the inbuilt URL shortener.

 ## How to run

To run the container:
````
docker run -it -p 8000:8000 smck83/qrcode-api
````

To run the container, with short.io integration:

````
 docker run -it -p 8000:8000 -e SHORTIO_APIKEY="<--  Your short.io API key-->" -e SHORTIO_DOMAIN="<-- Your short.io Domain Name -->" smck83/qrcode-api
````

To run the container, with inbuilt URL shortener:

````
 docker run -it -p 8000:8000 -e HOST_URL="<-- The public URL of your container -->" -e EXPAND_HOSTNAMES="True" -e ALLOWED_HOSTNAMES="therelayservice.com" smck83/qrcode-api
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
| HOST_URL | No | Default `None` :  If this is set, the inbuilt URL shortener will be used sharing shortlinks using this URL prefix e.g. `https://public.example.com` |
