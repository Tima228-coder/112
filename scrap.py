import requests
from bs4 import BeautifulSoup
import json


def detect_store(page):
    if "ctrs.com.ua" in page:
        return "ctrs"
    elif "rozetka" in page:
        return "rozetka"
    elif "foxtrot" in page:
        return "foxtrot"
    elif "moyo" in page:
        return "moyo"
    elif "comfy" in page:
        return "comfy"
    else:
        return None


class Scrapper:
    headers_dict = {
        "comfy": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        },
        "ctrs": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/118.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        "rozetka": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br"
        },
        "foxtrot": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.159 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br"
        },
        "moyo": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.159 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br"
        }
    }

    def __init__(self, page):
        self.page = page
        self.product_name = None
        self.price = None
        self.store = detect_store(page)

        if self.store:
            self.headers = self.headers_dict[self.store]
            self.scrape()

    def scrape(self):
        raise self.scrape

    def get_product_name(self):
        return self.product_name

    def get_price(self):
        return self.price

    def get_store(self):
        return self.store


class Comfy(Scrapper):
    def scrape(self):
        response = requests.get(self.page, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        script_tag = soup.find("script", type="application/ld+json")
        if script_tag:
            json_data = json.loads(script_tag.string)
            self.price = json_data.get("offers", {}).get("price", "Ціна не знайдена")
            self.product_name = json_data.get("name", "Назва не знайдена")
        else:
            self.product_name = "Не знайдена"
            self.price = "Не знайдена"


class Citrus(Scrapper):
    def scrape(self):
        response = requests.get(self.page, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        price_element = soup.find("div", class_="Price_price__KKCnw")
        if price_element:
            self.price = price_element.get("data-price", "Ціна не знайдена")
        else:
            self.price = "Ціна не знайдена"

        title_meta = soup.find("meta", {"property": "og:title"})
        if title_meta:
            self.product_name = title_meta.get("content", "Назва не знайдена")
        else:
            self.product_name = "Назва не знайдена"


class Rozetka(Scrapper):
    def scrape(self):
        response = requests.get(self.page, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("meta", property="og:title")
        if title_tag:
            self.product_name = title_tag["content"]

        price_tag = soup.find("p", class_="product-price__big product-price__big-color-red")
        if price_tag:
            self.price = price_tag.text.strip()
        else:
            self.price = "Ціна не знайдена"


class Foxtrot(Scrapper):
    def scrape(self):
        response = requests.get(self.page, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        script = soup.find("script", {"type": "application/ld+json"})
        if script:
            data = json.loads(script.string)
            if "hasVariant" in data:
                variant = data["hasVariant"][0]
                self.product_name = variant.get("name", "Не вказано")
                self.price = variant.get("offers", {}).get("price", "Не вказано")
            else:
                self.product_name = "Не вказано"
                self.price = "Не вказано"
        else:
            self.product_name = "Не вказано"
            self.price = "Не вказано"


class Moyo(Scrapper):
    def scrape(self):
        response = requests.get(self.page, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("meta", {"property": "og:title"})
        if title_tag:
            self.product_name = title_tag["content"]

        price_tag = soup.find("meta", {"itemprop": "price"})
        if price_tag:
            self.price = price_tag["content"]
        else:
            self.price = "Ціна не знайдена"

            demo_comfy = "https://comfy.ua/ua/smartfon-apple-iphone-16-pro-128gb-natural-titanium.html"
            demo_ctrs = "https://www.ctrs.com.ua/ru/smartfony/iphone-16-pro-128gb-natural-titanium-apple-752251.html"
            demo_rozetka = "https://rozetka.com.ua/apple-myng3sx-a/p448744745/"
            demo_foxtrot = ("https://www.foxtrot.com.ua/ru/shop/smartfoniy-i-mobilniye-telefoniy-apple-iphone-16-pro"
                            "-256gb-natural-titanium.html")
            demo_moyo = "https://www.moyo.ua/ua/smartfon_apple_iphone_16_pro_256gb_natural_titanium/600482.html"

            scrapers = [Comfy(demo_comfy), Citrus(demo_ctrs), Rozetka(demo_rozetka), Foxtrot(demo_foxtrot),
                        Moyo(demo_moyo)]

            for scraper in scrapers:
                print(f"Store: {scraper.get_store()}")
                print(f"Product Name: {scraper.get_product_name()}")
                print(f"Price: {scraper.get_price()}")
