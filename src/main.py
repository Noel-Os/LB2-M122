from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import stripe
import pdfkit
from datetime import datetime as d
from ftplib import FTP
import smtplib

SENDER = "m122osmanaj@gmail.com"
PASSWORD = "M122TestPW"

host = "ftp.byethost14.com"
username = "b14_31622177"
password = "neural123"
    
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
        <title>Title</title>
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

    </body>
    </html>
    
    """

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(html, r'documentation\Payment.pdf', configuration=config)


def send_email(recipient, subject, body):

    filename = r'documentation\Payment.pdf'
    msg = MIMEMultipart("alternative")
    part = MIMEText(body, 'html')
    msg.attach(part)
    #msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='Receipt.pdf')

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment", filename=filename
    )
    msg.attach(part)

    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = recipient
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    stripe.api_key = "sk_test_51KiDANElM3dtUv2KoZ7ttJQNgVlkOYDQnlVnl4etIKaEo0PEZFzIgT8znwHgrmAzj3VSJIDa64Uu1WbobPOcZFAb00Yzh1InKZ"

    #stripe.Customer.update()

    #createProduct()
    p = stripe.Product.list()
    #print(p["data"])

    payment = stripe.PaymentIntent.list()
    #print(payment["data"])

    #stripe.Customer.delete("cus_LaOjbIBdZt0Tlz")

    # stripe.Customer.modify("cus_LaOjbIBdZt0Tlz",
    #                        address=[
    #                            {
    #                                "city": "Bruettisellen",
    #                                "country": "Switzerland",
    #                                "line1": "Im Talacher 13",
    #                                "postal_code": "8306",
    #                            },
    #                        ],
    #                        )

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

    print(CustomerId)
    print(Customer["address"])

    city = str(stripe.Customer.retrieve(CustomerId)["address"]["city"])
    zip = str(stripe.Customer.retrieve(CustomerId)["address"]["postal_code"])
    street = str(stripe.Customer.retrieve(CustomerId)["address"]["line1"])
    country = str(stripe.Customer.retrieve(CustomerId)["address"]["country"])

    createPDF(stripe.PaymentIntent.retrieve("pi_3KnIjZElM3dtUv2K1qsvQn2j"))

    with FTP(host) as ftp:
        ftp.login(user=username, passwd=password)
        print(ftp.getwelcome())

        with open(r'documentation\Payment.pdf', 'rb') as f:
            ftp.storbinary('STOR ' + r'Payment.pdf', f)

    email_html = """
    <html>
      <head></head>
      <body>
        <p>
            Sehr geehrte/r """ + stripe.Customer.retrieve(CustomerId)["name"] + """<br>
            <br>
            Vielen Dank für Ihre Bestellung in unserem E-Shop.<br>
            Im Anhang erhalten Sie mit dieser Mail, eine Rechnung.<br>
            Ihre Bestellung ist zurzeit in bearbeitung, Sie können diese jederzeit unter folgendem <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ>Link</a> verfolgen.<br>
            <br>
            Mit freundlichen Grüssen<br>
            <br>
            Ihr E-Shop, Sheemo
        </p>
      </body>
    </html>
    """

    send_email("osmanaj.noel0@gmail.com", subject="Vielen Dank für Ihre Bestellung!", body=email_html)


    stripe.Customer.delete(Customer["id"])

    #print(stripe.Customer.list(limit=1))

    #print(stripe.Customer.list(limit=3))

    # stripe.PaymentIntent.create(
    #     amount=50,
    #     currency="chf",
    #     payment_method_types=["card"],
    # )

    t = stripe.PaymentIntent.retrieve("pi_3KnIjZElM3dtUv2K1qsvQn2j")

    #print(t['amount'])
