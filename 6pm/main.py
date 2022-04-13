import csv
import json
from csv import DictWriter

import lxml
import requests
from bs4 import BeautifulSoup

URL: str = "https://www.6pm.com/filters/null/WhUBgw_zHeAD0gaYHM0ZrxnhBuwcsw_iAgEL.zso?s=isNew/desc/goLiveDate/desc/recentpricesStyle/desc/&p=0"
HEADERS: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36", "Accept": "*/*"}

def get_all_url(url: str, headers: dict) -> list:
    req = requests.get(url, headers=headers)
    src: str = req.text
    
    soup = BeautifulSoup(src, "lxml")
    max_page: str = soup.find(class_="Ct-z").find_all("a")[-1].text

    print("parsing url...")
    all_card_href: list = []
    for page in range(int(max_page)):
        req2 = requests.get(f"{url[:-1]}{page}", headers=headers)
        src2: str = req2.text
        
        soup2 = BeautifulSoup(src2, "lxml")
        card_href = soup2.find_all(class_="Vh-z")
        all_card_href.extend(f'https://www.6pm.com{el["href"]}' for el in card_href)
    print("comlete")
    
    return all_card_href


def get_data(url_lst: list, headers: dict) -> None:
    title: list = ["name", "price", "MSRP", "href"]

    with open("6pm\RESULT.csv", 'w', newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(title)

    for count, url in enumerate(url_lst, start=1):
        req = requests.get(url, headers=headers)
        src: str = req.text

        soup = BeautifulSoup(src, "lxml")
        name = soup.find(class_ = "OM-z").text
        try: price = soup.find(class_ = "eJ-z jJ-z")["content"]
        except Exception: price = soup.find(class_ = "eJ-z")["content"]
        try: msrp = soup.find(class_ = "oJ-z").text[1:]
        except Exception: msrp = "-"

        card: dict = {"name": name, "price": price, "MSRP": msrp, "href": url}

        with open('6pm\RESULT.csv', 'a', newline='', encoding="utf-8") as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=title, delimiter=';')
            dictwriter_object.writerow(card)
            f_object.close()

        with open("6pm\RESULT.json", "a", encoding="utf-8") as file:
            json.dump(card, file, indent=4, ensure_ascii=False)

        print(f"{count}/{len(url_lst)}")
    

def main(url: str, headers: dict) -> None:
    all_url: list = get_all_url(url, headers)
    get_data(all_url, headers)


if __name__ == "__main__":
    main(URL, HEADERS)