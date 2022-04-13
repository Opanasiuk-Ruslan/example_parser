import csv

import lxml
import requests
from bs4 import BeautifulSoup

def get_num_page(url: str, headers: dict):


    req =  requests.get(url, headers=headers)
    src: str = req.text

    soup = BeautifulSoup(src, "lxml")
    num_pages: str = soup.find_all(class_ = "toolbar-number")[-1].text
    title_name: str = soup.find(class_ = "page-title").text.strip()
    return int(num_pages)//48+1, title_name.replace(" ", "_")


def get_data(url: str, headers: dict) -> str:
    num, title_name = get_num_page(url, headers)


    with open(f"511\{title_name}.csv", 'w', newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (   
                "name",
                "price",
                "id",
                "image",
                "href"
            )
        )

    for page in range(1, num+1):
        req = requests.get(url[:-1] + str(page), headers=headers)
        src: str = req.text

        soup = BeautifulSoup(src, "lxml")
        cards = soup.find_all(class_ = "product-item-info")
        for card in cards:
            name = card.find(class_ = "product details product-item-details").find(class_ = "product-item-link").text.strip()
            href = card.find("a").attrs["href"]
            try: id = card.find(class_ = "product details product-item-details").find(class_ = "price-box price-final_price")["data-product-id"]
            except: id = "-"
            image = card.find(class_ = "product-image-wrapper").img["src"]
            try: price = card.find(class_ = "price-box price-final_price").find(class_ = "price").text.replace("€", "")
            except: price = "-"

            with open(f"511\{title_name}.csv", 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    (   
                        name,
                        price,
                        id,
                        image,
                        href
                    )
                )
    return f"511\{title_name}.csv"