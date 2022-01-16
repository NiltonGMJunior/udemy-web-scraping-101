import json
from lxml import html
import requests


def get_items(url, headers):
    resp = requests.get(
        url=url,
        headers=headers
    )
    tree = html.fromstring(html=resp.text)
    item_urls = tree.xpath("//a[starts-with(@href, 'https://www.ebay.com/itm/')]/@href")
    return item_urls

def scrape_item_data(url, headers):
    resp = requests.get(
        url=url,
        headers=headers
    )

    tree = html.fromstring(html=resp.text)

    title = tree.xpath("//h1[@id='itemTitle']/text()")
    info = tree.xpath("//div[string()='Features:' and contains(@class, 'ux-labels-values__labels-content')]/parent::div/following-sibling::div[1]/div/div/span/text()")
    watcher_count = tree.xpath("//span[contains(@class, 'w2b-sgl') and contains(string(), 'watchers')]/text()")

    return {
        'title': title[0] if title else None,
        'url': url,
        'info': info[0] if info else None,
        'watcher_count': int("".join(list(filter(lambda x: x.isdigit(), watcher_count[0])))) if watcher_count else None,
    }

def write_data_to_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    # NOTE: Since the trending items page is no longer available, this project will use the Global Deals page instead.
    # NOTE: This should only work properly when the content-language header is set to English in the response.
    global_deals_url = "https://www.ebay.com/globaldeals"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    item_urls = list(set(get_items(global_deals_url, headers)))

    data = []
    for item_url in item_urls:
        item_data = scrape_item_data(item_url, headers)
        data.append(item_data)

    write_data_to_json('output.json', data)
