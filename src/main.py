import ftplib
import stripe
import pdfkit
from html.parser import HTMLParser
from datetime import datetime as d

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
