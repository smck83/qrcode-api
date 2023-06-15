# qrcode-api
 An API built using fastAPI that returns an auto-generated QR code when a URL is passed into `message`

 e.g. 
 `https://localhost:8000/generate-qr-code?message=https://example.com`

 Support for URL shortener service `short.io` has been added. This allows you to keep the QR code version low, which means a more simple QR code.

 TO use `https://short.io` you will need to parse ENVIRONMENT VARIABLES:

 `SHORTIO_APIKEY` and `SHORTIO_DOMAIN`

 e.g.
````
 docker run -it -p 8000:8000 -e SHORTIO_APIKEY="<--  Your short.io API key-->" -e SHORTIO_DOMAIN="<-- Your short.io Domain Name -->" smck83/qrcode-api
 ````

If you don't want to use URL shortening and are happy for larger `version` QR codes; you can run vai:

````
docker run -it -p 8000:8000 smck83/qrcode-api
````



