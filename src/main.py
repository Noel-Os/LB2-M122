import json
from fpdf import FPDF, HTMLMixin
import stripe

def createPDF(data):
    html = """
    <H1 align="center">html2fpdf</H1>
    <h2>Basic usage</h2>
    <p>You can now easily print text mixing different
    styles : <B>bold</B>, <I>italic</I>, <U>underlined</U>, or
    <B><I><U>all at once</U></I></B>!<BR>You can also insert links
    on text, such as <A HREF="http://www.fpdf.org">www.fpdf.org</A>,
    or on an image: click on the logo.<br>
    <center>
    <A HREF="http://www.fpdf.org"><img src="tutorial/logo.png" width="104" height="71"></A>
    </center>
    <h3>Sample List</h3>
    <ul><li>option 1</li>
    <ol><li>option 2</li></ol>
    <li>option 3</li></ul>

    <table border="0" align="center" width="50%">
    <thead><tr><th width="30%">Header 1</th><th width="70%">header 2</th></tr></thead>
    <tbody>
    <tr><td>cell 1</td><td>cell 2</td></tr>
    <tr><td>cell 2</td><td>cell 3</td></tr>
    </tbody>
    </table>
    """

    class MyFPDF(FPDF, HTMLMixin):
        pass

    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font('arial', '', 14)
    pdf.write_html(html)
    pdf.output("./documentation/Payment.pdf")


    # pdf = FPDF()
    #
    # pdf.add_page()
    #
    # pdf.set_font("Arial", size=40, style="B")
    #
    # pdf.cell(200, 10, txt="Payment Receipt",
    #          ln=1, align='C', )
    #
    # pdf.set_font("Arial", size=30, style="B")
    #
    # pdf.cell(100, 30, txt="Bestellung an:",
    #         ln=2, align='L')
    #
    # pdf.set_font("Arial", size=15, style="B")
    #
    # pdf.cell(10, 10, txt="Name:",
    #         ln=3, align='L')
    #
    # pdf.cell(50, 10, txt="Adresse:",
    #          ln=4, align='L')
    #
    # pdf.cell(50, 10, txt="Datum:",
    #          ln=4, align='L')
    #
    # pdf.cell(50, 10, txt="Bezahlungs Methode:",
    #          ln=4, align='L')
    #
    # pdf.set_font("Arial", size=15)
    #
    # pdf.cell(10, 5, txt="Test Test",
    #          ln=3, align='C')

if __name__ == '__main__':
    stripe.api_key = "sk_test_51KiDANElM3dtUv2KoZ7ttJQNgVlkOYDQnlVnl4etIKaEo0PEZFzIgT8znwHgrmAzj3VSJIDa64Uu1WbobPOcZFAb00Yzh1InKZ"

    createPDF(stripe.PaymentIntent.retrieve("pi_3KnIjZElM3dtUv2K1qsvQn2j"))

    #stripe.Customer.create(
    #    balance=100,
    #    description="My First Test Customer (created for API docs)",
    #)

    #print(stripe.Customer.list(limit=3))

    # stripe.PaymentIntent.create(
    #     amount=50,
    #     currency="chf",
    #     payment_method_types=["card"],
    # )

    t = stripe.PaymentIntent.retrieve("pi_3KnIjZElM3dtUv2K1qsvQn2j")

    print(t['amount'])
