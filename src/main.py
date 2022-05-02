from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import stripe
import pdfkit
from datetime import datetime as d
from ftplib import FTP
import smtplib

RECEIVER = "osmanaj.noel0@gmail.com"
SENDER = "m122osmanaj@gmail.com"
PASSWORD = "M122TestPW"

host = "ftp.byethost7.com"
username = "b7_31642774"
password = "FTPM122"

ProductId = ""
PriceId = ""

amount = 5

CustomerId = ""
city = ""
zip = ""
street = ""
country = ""

def createProduct():
    stripe.Product.create(name="Nintendo Switch")

def createPDF(data):

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PDF</title>
        <style>
        th, td {
          padding: 5px;
          text-align: left;
        }
        </style>
    </head>
    <body>
    <h1 align="center">Payment Receipt</h1>

    <table style="width:100%">
        <tbody>
            <tr>
                <th><h2>Invoice To</h2></th>
            </tr>
            <tr>
                <th>Name</th>
                <td>""" + stripe.Customer.retrieve(CustomerId)["name"] + """</td>
            </tr>
            <tr>
                <th>Address</th>
                <td>""" + street + "<br>" + city + " " + zip + "<br>" + country + """</td>
            </tr>
            <tr>
                <th>Date</th>
                <td>""" + d.now().strftime("%H:%M:%S %Y-%m-%d") + """</td>
            </tr>
        </tbody>
    </table>

    <hr>
    
    <th><h2>Products</h2></th>
    
    <table style="width:100%">
    
        <tbody>
        
            <tr>
                <th>Product</th>
                <th>Amount</th>
                <th>Price per Unit</th>
                <th>Price</th>
            </tr>
    """

    for product in stripe.Product.list():

        price = stripe.Price.search(
            query="product:'" + product["id"] + "'",
        )

        for p in price:
            PriceId = p["id"]

        html = html + """
        <tr>
            <td>""" + product["name"] + """</td>
            <td>""" + str(amount) + """</td>
            <td>""" + str(format(stripe.Price.retrieve(PriceId)["unit_amount"] / 100, '.02f')) + """</td>
            <td>""" + str(format((stripe.Price.retrieve(PriceId)["unit_amount"] * amount) / 100, '.02f')) + """</td>
        </tr>"""
    html = html + """
          
        </tbody>
    
    </table>
    
    </body>
    </html>
    
    """

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(html, r'..\documentation\Payment.pdf', configuration=config)


def send_email(subject, body):

    filename = r'..\documentation\Payment.pdf'
    msg = MIMEMultipart("alternative")
    part = MIMEText(body, "html")
    msg.attach(part)

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment", filename='Payment_' + stripe.Customer.retrieve(CustomerId)["name"] + '_' + d.now().strftime("%H:%M:%S %Y-%m-%d") + '.pdf'
    )
    msg.attach(part)

    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    stripe.api_key = "sk_test_51KiDANElM3dtUv2KoZ7ttJQNgVlkOYDQnlVnl4etIKaEo0PEZFzIgT8znwHgrmAzj3VSJIDa64Uu1WbobPOcZFAb00Yzh1InKZ"

    payment = stripe.PaymentIntent.list()

    Customer = stripe.Customer.create(
        balance=100,
        description="Test Customer",
        email="osmanaj.noel0@gmail.com",
        name="Noel Osmanaj",
        address={
                "city": "Bruettisellen",
                "country": "CH",
                "line1": "Im Talacher 13",
                "postal_code": "8306",
        },
    )
    CustomerId = Customer["id"]

    product = stripe.Product.search(
        query="name:'Nintendo Switch'",
    )

    for p in product:
        ProductId = p["id"]

    city = str(stripe.Customer.retrieve(CustomerId)["address"]["city"])
    zip = str(stripe.Customer.retrieve(CustomerId)["address"]["postal_code"])
    street = str(stripe.Customer.retrieve(CustomerId)["address"]["line1"])
    country = str(stripe.Customer.retrieve(CustomerId)["address"]["country"])

    createPDF(stripe.PaymentIntent.retrieve("pi_3KnIjZElM3dtUv2K1qsvQn2j"))

    with FTP(host) as ftp:
        ftp.login(user=username, passwd=password)

        with open(r'C:\Users\User\Desktop\Aufgaben\TBZ\Module\Modul 122\LB-2\LB2-M122\documentation\Payment.pdf', 'rb') as f:
            ftp.storbinary('STOR ' + r'Orders/Payment_' + stripe.Customer.retrieve(CustomerId)["name"] + '_' + d.now().strftime("%H:%M:%S %Y-%m-%d") + '.pdf', f)

    email_html = """\
    
    <html>
      <body>
        <p>
            Sehr geehrte/r """ + stripe.Customer.retrieve(CustomerId)["name"] + """<br>
            <br>
            Vielen Dank für Ihre Bestellung in unserem E-Shop.<br>
            Im Anhang erhalten Sie mit dieser Mail, eine Rechnung.<br>
            Ihre Bestellung ist zurzeit in bearbeitung, Sie können diese jederzeit unter folgendem <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Link</a> verfolgen.<br>
            <br>
            Mit freundlichen Grüssen<br>
            <br>
            Ihr E-Shop, Sheemo
        </p>
      </body>
    </html>
    """

    send_email(subject="Vielen Dank für Ihre Bestellung!", body=email_html)

    stripe.Customer.delete(Customer["id"])

    t = stripe.PaymentIntent.retrieve("pi_3KnIjZElM3dtUv2K1qsvQn2j")

