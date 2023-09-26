# Add QR Code Phishing Simulation to Mimecast Awareness Training
````
DISCLAIMER: This is an unofficial and unaffiliated instruction on how Mimeast Phishing Simulation can be customised using qrcode-api to support QR code phishing simulation.
````

It is possible to host your own QR Code generator API endpoint and point Mimecast Awareness Training Phishing Simulation to test your users with QR Codes.


The Mimecast phishing simulation template variable is `[rawlink]` which will be replaced with a unique URL upon delivery to be able to attribute an end user, receiving a phishing simulation e-mail and clicking the unique link.

The value of `\[rawlink\]` can easily be sent to a web endpoint when the phishing simulation loads to request a QR Code image such as [qrcode-api](https://github.com/smck83/qrcode-api/)https://github.com/smck83/qrcode-api/ that 
