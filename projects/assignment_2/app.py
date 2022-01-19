import re
from urllib.parse import urljoin

from lxml import html
import requests


def get_text(element):
    try:
        return element.pop(0)
    except:
        return ""


def scrape(url, headers):
    """Generator that scrapes the given IMDB url and yields movie details

    Args:
        url (str): The IMDB url to scrape
        headers (dict): The headers to use for the HTTP request

    Yields:
        dict: The movie details
    """
    resp = requests.get(url, headers=headers)
    tree = html.fromstring(resp.content)
    movie_list = tree.xpath(
        "//div[@class='lister-list']/div[contains(@class,'lister-item')]")
    for movie in movie_list:
        movie_content = movie.xpath(".//div[@class='lister-item-content']")[0]
        movie_details = {
            "title": get_text(movie_content.xpath(".//h3[@class='lister-item-header']/a/text()")),
            "release_year": int(re.sub(r"[^\d]", "", get_text(movie_content.xpath(".//h3[@class='lister-item-header']/span[contains(@class,'lister-item-year')]/text()")))),
            "duration_min": int(re.sub(r"[^\d]", "", get_text(movie_content.xpath(".//p/span[contains(@class,'runtime')]/text()")))),
            "genres": re.sub(r"[\s]", "", get_text(movie_content.xpath(".//p/span[contains(@class,'genre')]/text()"))).split(","),
            "rating": float(get_text(movie_content.xpath(".//div[contains(@class,'ratings-bar')]/div[contains(@class,'ratings-imdb-rating')]/strong/text()"))),
        }
        yield movie_details

    next_page = tree.xpath("//a[contains(@class,'next-page')]/@href")
    if next_page:
        next_page_url = urljoin(base=url, url=next_page[0])
        yield from scrape(next_page_url, headers)


if __name__ == "__main__":
    movies = scrape(url="https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv",
                    headers={"User-Agent": "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
                             "Accept-Language": "en-US,en;q=0.5"})
    for movie in movies:
        print(movie)
