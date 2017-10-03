import requests
import lxml.html

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
}

r_session = requests.Session()

# Paste your cookies to avoid bot protection
cookies = {
}


def get_product_specs(
        product_url="https://market.yandex.ru/product/1727685734"):
    response = r_session.get(product_url, headers=headers, cookies=cookies)
    html_doc = response.content.decode("utf-8")
    tree = lxml.html.fromstring(html_doc)
    title = tree.xpath('//h1[contains(@class,"title")]')[0].text
    ul = tree.xpath('//ul[contains(@class,"n-product-spec-list")]')[0]
    spec_list = list(map(lambda l: l.text, list(ul)))
    price = tree.xpath('//span[@class="price"]')[0].text
    img_url = tree.xpath(
        '//img[contains(@class,"n-gallery__image")]')[0].attrib['src']
    return (title, spec_list, price, img_url)


def get_product_list():
    category_url = "https://market.yandex.ru/catalog/54544/list?local-offers-first=0&deliveryincluded=0&onstock=1"

    response = r_session.get(category_url, headers=headers, cookies=cookies)
    html_doc = response.content.decode("utf-8")
    tree = lxml.html.fromstring(html_doc)

    a_nodes = tree.xpath('//a[contains(@class,"snippet-card__header-link")]')
    urls = list(map(lambda l: l.attrib['href'], a_nodes))
    urls = list(map(lambda u: 'https://market.yandex.ru' + u, urls))
    return urls


# if __name__ == "__main__":
#    print([get_product_specs(url) for url in get_product_list()])
