from lxml import html
import requests
from urllib.parse import urljoin
from pymongo import MongoClient
import ssl


def insert_to_db(list_currencies):
    client = MongoClient("mongodb://admin:admin@coinmarketcap-scraper-shard-00-00.ethua.mongodb.net:27017,coinmarketcap-scraper-shard-00-01.ethua.mongodb.net:27017,coinmarketcap-scraper-shard-00-02.ethua.mongodb.net:27017/currencies?ssl=true&replicaSet=atlas-p3ykz1-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client["currencies"]
    collection = db["price"]
    for currency in list_currencies:
        exists = collection.find_one({"_id": currency["_id"]})
        if exists:
            collection.replace_one({"_id": currency["_id"]}, currency)
        else:
            collection.insert_one(currency)
    client.close()

def get(list_elements):
    try:
        return list_elements.pop(0)
    except:
        return ""


all_currencies = []


def scrape(url):
    resp = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }
    )

    tree = html.fromstring(resp.content)

    currencies = tree.xpath("//table[@id='currencies']/tbody/tr")
    for currency in currencies:
        c = {
            "_id": int(get(currency.xpath(".//td[1]/text()"))),
            "name": get(currency.xpath(".//td[2]/a[contains(@class,'currency-name-container')]/text()")),
            "market_cap": get(currency.xpath(".//td[3]/@data-usd")),
            "price": get(currency.xpath(".//td[4]/a/@data-usd")),
            "change (24h)": get(currency.xpath(".//td[7]/@data-percentusd")),
        }

        all_currencies.append(c)
        print(c)

    next_page = tree.xpath("//div[@class='pull-right']/ul[contains(@class, 'pagination')]/li/a[contains(text(), 'Next')]/@href")

    if next_page:
        next_page_url = urljoin(base=url, url=next_page[0])
        scrape(url=next_page_url)


if __name__ == "__main__":
    scrape(url="http://web.archive.org/web/20190312000208/https://coinmarketcap.com/")
    insert_to_db(list_currencies=all_currencies)
