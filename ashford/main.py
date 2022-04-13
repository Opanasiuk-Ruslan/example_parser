import csv
import json
from csv import DictWriter

import lxml
import requests
from bs4 import BeautifulSoup

URL: str = "https://www.ashford.com/womens-watches.html?product_list_order=weekly_deals~desc&p=1"
HEADERS: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36", "Accept": "*/*"}

def get_all_url(url: str, headers: dict) -> list:
    req = requests.get(url, headers=headers)
    src: str = req.text

    soup = BeautifulSoup(src, "lxml")
    all_pages: str = soup.find(class_ = "toolbar-amount").text.split(" ")[-2]
    print("parsing url...")
    all_url: list = []

    for page in range(1, int(all_pages)//40+2):
        new_url = url[:-1] + str(page)

        req2 = requests.get(new_url, headers=headers)
        src2: str = req2.text

        soup2 = BeautifulSoup(src2, "lxml")
        href = soup2.find_all(class_ = "product-item-info")

        all_url.extend(el.a["href"] for el in href[:40])
        if len(all_url) > 100: break
    print("comlete")
    return all_url[:100]


def get_data(url_lst: list, headers: dict) -> None:
    title: list = {"Name", "Movement", "Case Width", "Water Resistance", "Features", "Price", "Href"}
    with open("ashford\RESULT.csv", 'w', newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(title)

    for count, url in enumerate(url_lst, start=1):
        req = requests.get(url, headers=headers)
        src: str = req.text

        soup = BeautifulSoup(src, "lxml")
        name = soup.find(class_ = "f-17 qvPrdURL link-black text-capitalize").text
        info = soup.find(class_ = "product-description").find_all("li")
        lst_info: list = [el.text.split(":") for el in info]
        price = soup.find(class_ = "d-flex align-items-end justify-content-flex-start text-red mt-3").find(class_ = "price").text

        card: dict = {"Name": name, "Movement": "-", "Case Width": "-", "Water Resistance": "-", "Features": "-", "Price": price, "Href": url}
        for el in lst_info:
            if len(el) == 2: card[el[0].strip()] = el[-1].strip()

        with open("ashford\RESULT.csv", 'a', newline='', encoding="utf-8") as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=title, delimiter=';')
            dictwriter_object.writerow(card)
            f_object.close()

        with open("ashford\RESULT.json", "a", encoding="utf-8") as file:
            json.dump(card, file, indent=4, ensure_ascii=False)

        print(f"{count}/{len(url_lst)}")


def main(url: list, headers: dict) -> None:
    url_lst = get_all_url(url, headers)
    get_data(url_lst, headers)


if __name__ == "__main__":
    main(URL, HEADERS)