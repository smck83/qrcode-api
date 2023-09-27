# Add QR Code Phishing Simulation to Mimecast Awareness Training
````
DISCLAIMER: This is an unofficial, unsupported and unaffiliated instruction on how Mimeast Phishing Simulation can be customised using qrcode-api to support QR code phishing simulation.
````

It is possible to host your own QR Code generator API endpoint and point Mimecast Awareness Training Phishing Simulation to test your users with QR Codes.


The Mimecast phishing simulation template variable to track an end user clicking a link is `[rawlink]` which will be dynamically replaced with a unique URL upon delivery to be able to attribute an end user, clicking (or in this case, scanning) the unique link.

The value of `[rawlink]` can be passed to a web endpoint when the phishing simulation e-mail loads in an end users mailbox client (Outlook, OWA etc) to request a QR Code image such as [qrcode-api](https://github.com/smck83/qrcode-api/)

## QR Code Only
````
<img src='https://yourpublic.hostname.com/generate-qr-code?message=[rawlink]' />
````
## Hyperlinked QR Code
````
<a href=[rawlink]>
<img src='https://yourpublic.hostname.com/generate-qr-code?message=[rawlink]' />
</a>
````

# Google Charts
Google Charts provides a publicly available GET endpoint that can receive a string and return a QR code (like qrcode-api). This could also be used, however unlike [qrcode-api](https://github.com/smck83/qrcode-api/) this API does not shorten URL's. The string length of `[rawlink]` is ~440 characters which will result in a very large QR code if not first shortened, but will still work.

## QR Code Only

````
<img src='https://chart.googleapis.com/chart?cht=qr&chs=200x200&&chld=M|1&chl=[rawlink]' />
````

## Hyperlinked QR Code

````
<a href=[rawlink]>
<img src='https://chart.googleapis.com/chart?cht=qr&chs=200x200&&chld=M|1&chl=[rawlink]' />
</a>
````
