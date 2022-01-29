import requests

from lxml import html

def get_text(elem):
    if elem:
        return elem[0]
    else:
        return ''

script = '''
    function main(splash, args)
    headers = {
        ['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
        ['cookie'] = 'gb_testCookieId=rtpppnifudjo1642971503214; gb_lang=en; gb_pipeline=GB; _gcl_au=1.1.1963747731.1642971503; WEBF_predate=1642971606; WEBF_guid=b04f-c851498c61a0-59a1-484b-8c8c-010a82a56026_1642971503; cdn_countryCode=; gb_countryCode=US; aff_mss_info_bak={"bak":"bak"}; reffer_channel=; landingUrl=https://www.gearbest.com/; gb_soa_www_session=eyJpdiI6IkNaSmJWekpZZVhMbnZrRXl3cjR4NVE9PSIsInZhbHVlIjoic1YrY280d2JtQk9id2lBd2dES1IxWnU5ZXhoYUI1K3UyVlVtQm9QbkVxSEloS1VoZHEzb2NVTU54aURPVHdDOXo0UHdRXC81NXBWRmFTWUlyaFluUFlBPT0iLCJtYWMiOiJmNTU4MzNhZTQ2NDkxNjczN2MzNjc3NmVhMDgxOGE2MDI2OWIzZmRkM2UxODM4OTI4MjUxN2ZhNTBkZDE4ZTBlIn0%3D; gb_currencyCode=USD; gb_vsign=a2cb64c41d5e3562e3618c5733fdce9ce6e1c01a; _ga=GA1.2.737376847.1642971504; _gid=GA1.2.2030965516.1642971504; _fbp=fb.1.1642971504602.840867686; gb_pf=%7B%22rp%22%3A%22originalurl%22%2C%22lp%22%3A%22https%3A%2F%2Fwww.gearbest.com%2Fflash-sale.html%22%2C%22wt%22%3A1642971606696%7D; globalegrow_user_id=dca259ca-7ebd-ad1c-a92f-0370ab6c386c; globalegrowbigdata2018_globalegrow_session_id=0d98d607-9210-a26c-bac5-f6f08ddf51ad; od=tgrerkasjzxe1642971506015; osr_referrer=originalurl; osr_landing=https%3A%2F%2Fwww.gearbest.com%2Fflash-sale.html; gb_fcm=0; gb_fcmPipeLine=GB; gb_userinfo=eyJ1c2VyIjp7InVzZXJOYW1lIjoiIiwiZW1haWwiOiIiLCJhdmF0YXIiOiIiLCJpc05ld1VzZXIiOjAsInVzZXJJZCI6IjAifSwiY29sbGVjdCI6MCwiY2FydENvdW50IjowLCJpc0xvZ2luIjpmYWxzZSwidGlja2V0Q291bnQiOjAsInNpdGVNZXNzYWdlVGltZUludGVydmFsIjowfQ%3D%3D; _dc_gtm_UA-48073707-1=1; _gat_UA-48073707-11=1; globalegrowbigdata2018_globalegrow_session_id_0d98d607-9210-a26c-bac5-f6f08ddf51ad=false; _uetsid=344d03707c8f11ec9ca9311aad7104b0; _uetvid=344d1e407c8f11ec8e8b7770a0d29b52',
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
    'url': 'https://web.archive.org/web/20201109040757/https://www.gearbest.com/flash-sale.html',
})

tree = html.fromstring(html=resp.content)

deals = tree.xpath("//li[contains(@class, 'goodsItem')]/div[@class='goodsItem_content']")
for deal in deals:
    product = {
        'name': get_text(deal.xpath(".//div[@class='goodsItem_title']/a/text()")).strip(),
        'url': get_text(deal.xpath(".//div[@class='goodsItem_title']/a/@href")),
        'original_price': get_text(deal.xpath(".//div[@class='goodsItem_delete']/del/@data-currency")),
        'discounted_price': get_text(deal.xpath(".//div[@class='goodsItem_detail']/span/@data-currency")),
    }

    print(product)