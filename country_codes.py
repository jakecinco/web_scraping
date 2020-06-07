import requests
from bs4 import BeautifulSoup


def get_country_code(code_length: int) -> int:
    try:
        url = "https://www.iban.com/country-codes"
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        codes = []
        for i in soup.find_all("td"):
            x = i.text
            codes.append(x) if len(x) == code_length else None
        return codes
    except ValueError as e:
        print("Incorrect value entered: " + e)
