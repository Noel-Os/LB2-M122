import requests
from requests.auth import HTTPBasicAuth

if __name__ == '__main__':
    response = requests.get("https://api.stripe.com/v1/customers",
    auth=HTTPBasicAuth('sk_test_51KiDANElM3dtUv2KoZ7ttJQNgVlkOYDQnlVnl4etIKaEo0PEZFzIgT8znwHgrmAzj3VSJIDa64Uu1WbobPOcZFAb00Yzh1InKZ', ''))

    print(response.json())
