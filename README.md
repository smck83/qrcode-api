# qrcode-api
 An API built using fastAPI that returns an auto-generated QR code when a URL is passed into `message`

 e.g. 
 `https://localhost:8000/generate-qr-code?message=https://example.com`

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
 docker run -it -p 8000:8000 -e ALLOWED_HOSTNAMES="therelayservice.com" smck83/qrcode-api
````

Where `ALLOWED_HOSTNAMES` can have 1 or many (space seperated) allowed hostnames that the API will check the passed URL against. This is currently at the root level only e.g. If message= contained a URL with website.com.au, `com.au` would need to be in the `ALLOWED_HOSTNAMES` list, however it wouldnt be hard to make this configurable.
