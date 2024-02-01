# Add QR Code Phishing Simulation to Mimecast Awareness Training
````
DISCLAIMER: This is an unofficial, unsupported and unaffiliated instruction on how Mimecast Phishing Simulation can be customised using qrcode-api to support QR code phishing simulation.
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
# Alternatives to hosting [qrcode-api](https://github.com/smck83/qrcode-api/)

## Google Charts
Google Charts provides a publicly available GET endpoint that can receive a string and return a QR code (like qrcode-api). This could also be used, however unlike [qrcode-api](https://github.com/smck83/qrcode-api/) this API does not shorten URL's. The string length of `[rawlink]` is ~440 characters which will result in a very large QR code if not first shortened, but will still work.

#### QR Code Only

````
<img src='https://chart.googleapis.com/chart?cht=qr&chs=200x200&&chld=M|1&chl=[rawlink]' />
````

#### Hyperlinked QR Code

````
<a href=[rawlink]>
<img src='https://chart.googleapis.com/chart?cht=qr&chs=200x200&&chld=M|1&chl=[rawlink]' />
</a>
````

## Google Charts
Google Charts provides a publicly available GET endpoint that can receive a string and return a QR code (like qrcode-api). This could also be used, however unlike [qrcode-api](https://github.com/smck83/qrcode-api/) this API does not shorten URL's. The string length of `[rawlink]` is ~440 characters which will result in a very large QR code if not first shortened, but will still work. Documentation : https://developers.google.com/chart/infographics/docs/qr_codes

#### QR Code Only

````
<img src='https://chart.googleapis.com/chart?cht=qr&chs=200x200&&chld=M|1&chl=[rawlink]' />
````

#### Hyperlinked QR Code

````
<a href=[rawlink]>
<img src='https://chart.googleapis.com/chart?cht=qr&chs=200x200&&chld=M|1&chl=[rawlink]' />
</a>
````

## QuickChart
QuickChart provides a publicly available GET endpoint that can receive a string and return a QR code (like qrcode-api). This could also be used, however unlike [qrcode-api](https://github.com/smck83/qrcode-api/) this API does not shorten URL's. The string length of `[rawlink]` is ~440 characters which will result in a very large QR code if not first shortened, but will still work. Documentation : https://quickchart.io/qr-code-api/

#### QR Code Only

````
<img src='https://quickchart.io/qr?margin=2&size=200&text=[rawlink]' />
````

#### Hyperlinked QR Code

````
<a href=[rawlink]>
<img src='https://quickchart.io/qr?margin=2&size=200&text=[rawlink]' />
</a>
````
## Add hostname(s) to Trusted Sites
By default, Outlook will not load images externally hosted. To resolve this, without configuring Outlook to load 'ALL' external images add the hostnames of the endpoint(s) you decide to use to `Trusted Sites`
Manually via:

````
Open Control Panel.
Click or double-click the Internet Options icon.
In the Internet Properties window, click the Security tab.
Select Trusted sites and click the Sites button.
Type the address of the QR Code endpoint hostname in the Add this website to field text box (e.g. https://yourpublic.hostname.com/ or https://chart.googleapis.com/)
Click the Add button and click OK to save the addition to the site.
````
Or using Group Policy (GPO) using this ManageEngine instruction on [Securing zone levels in Internet Explorer](https://blogs.manageengine.com/active-directory/2018/08/02/securing-zone-levels-internet-explorer.html)https://blogs.manageengine.com/active-directory/2018/08/02/securing-zone-levels-internet-explorer.html.
