import requests
from urllib.parse import urljoin

import click
from lxml import html

def get_text(elem):
    if elem:
        return elem[0]
    else:
        return ''

def scrape_upcoming_flights(url):
    script = '''
        function main(splash, args)
            headers = {
                ['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
                ['cookie'] = '_ga=GA1.2.69796563.1642970173; _gid=GA1.2.649257702.1642970173; __hstc=53236791.a5541eae59e1bca6d95e9daf47717af6.1642970174545.1642970174545.1642984566563.2; hubspotutk=a5541eae59e1bca6d95e9daf47717af6; __hssrc=1; _gcl_au=1.1.1826331201.1642970175; __gads=ID=61a524afd3cc84ce-22aa5122efb3007f:T=1642980975:S=ALNI_MYewETJNeAEIX1r0KJdHH8z1krPqA; __qca=P0-1516667383-1642970176609; w_locale=en_US; _pbjs_userid_consent_data=3524755945110770; _pubcid=4619e7b5-76ea-43e7-a7cf-7cdae0f2fe6c; __rtgt_sid=kyryl87r00etdc; __hssc=53236791.7.1642984566563; _gat=1',
                ['Accept-Language'] = 'en-US,en;q=0.5',
            }
            splash:set_custom_headers(headers)
            splash.private_mode_enabled = false
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            return splash:html()
        end
    '''

    resp = requests.post(url='http://localhost:8050/execute', json={
        'lua_source': script,
        'url': url,
    })

    tree = html.fromstring(html=resp.content)
    print(resp.content)
    # Check if the "Upcoming Flights" table is present
    upcoming_flights = tree.xpath("//div[@class='flightPageDataTableHeadingContainer']/h2[contains(text(), 'Upcoming')]/parent::div/following-sibling::div[@class='flightPageDataTableContainer'][1]")
    if upcoming_flights:
        flights = upcoming_flights[0].xpath(".//div[contains(@class, 'flightPageDataTable')]/div[contains(@class,'flightPageDataRowTall')]")
        for flight in flights:
            columns = flight.xpath(".//div[contains(@class, 'flightPageActivityLogData')]")
            date = get_text(columns[0].xpath(".//span/text()"))
            departure_time = get_text(columns[1].xpath(".//div/div/span[1]/em/span/text()"))
            departure_airport = get_text(columns[1].xpath(".//div/div/span[2]/a/@data-tip"))
            departure_airport_abv = get_text(columns[1].xpath(".//div/div/span[2]/a/text()"))
            arrival_time = get_text(columns[2].xpath(".//div/div/span[1]/em/span/text()"))
            arrival_airport = get_text(columns[2].xpath(".//div/div/span[2]/a/@data-tip"))
            arrival_airport_abv = get_text(columns[2].xpath(".//div/div/span[2]/a/text()"))
            aircraft = get_text(columns[3].xpath(".//span/@data-tip"))
            aircraft_abv = get_text(columns[3].xpath(".//span/text()"))
            duration = get_text(columns[4].xpath(".//em/text()"))

            yield {
                "Aircraft": aircraft,
                "Aircraft Abbreviation": aircraft_abv,
                "Date": date,
                "Departure Time": departure_time,
                "Departure Airport": departure_airport,
                "Departure Airport Abbreviation": departure_airport_abv,
                "Arrival Time": arrival_time,
                "Arrival Airport": arrival_airport,
                "Arrival Airport Abbreviation": arrival_airport_abv,
            }

@click.command()
@click.option("--flightcode", default="HOP1319", help="Flight code to scrape")
def scrape(flightcode):
    url = urljoin("https://flightaware.com/live/flight", flightcode)
    for flight in scrape_upcoming_flights(url):
        print(flight)

if __name__ == "__main__":
    scrape()