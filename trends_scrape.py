import re
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from country_codes import get_country_code


def fetch_xml(country_code):
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={country_code}"
    start = time.time()
    response = requests.get(url)
    response_time = float("{:.2f}".format(time.time() - start))
    print(f"The request took {response_time}s to complete.")
    return response.content


def get_trends(country_code):
    xml_document = fetch_xml(country_code)
    soup = BeautifulSoup(xml_document, "lxml")

    titles = soup.find_all("title")
    main_title = titles[0].text
    pubdates = []
    for s in soup.select("channel"):
        for ss in s.find_all("title"):
            # print(ss.text)
            for sss in ss.find_next_siblings("pubdate"):
                dt_obj = datetime.strptime(sss.text, "%a, %d %b %Y %H:%M:%S %z")
                pubdates.append(dt_obj)
                # print(dt_obj.date() == datetime.today().date())

    print("=====================================")
    print(main_title)
    print(datetime.today().date().strftime("%A, %d-%b-%Y"))
    print("=====================================")
    approx_traffic = soup.find_all("ht:approx_traffic")
    return {title.text: (re.sub("[+,]", "", traffic.text), pubdate)
            for title, traffic, pubdate in zip(titles[1:], approx_traffic, pubdates)}


def print_trends(arg):
    trends = get_trends(arg)
    n = 1
    for trend, value in trends.items():
        print(f"{n}. {trend} - {value[0]} hits") if value[1].date() == datetime.today().date() else None
        n += 1


if __name__ == '__main__':
    inp = input("Enter a 2-letter country code to start search: ")
    code_length = 2
    code_list = get_country_code(code_length)

    while True:
        if len(inp) == code_length and inp.upper() not in code_list:
            print(inp)
            inp = input("Please enter a valid country code: ")
        elif len(inp) != code_length:
            inp = input("Please enter a 2-letter country code.\n"
                        "A list of alpha-2 codes can be found here: \n"
                        "https://www.iban.com/country-codes\n"
                        "Country code: ")
        else:
            break

    print_trends(inp.upper())

