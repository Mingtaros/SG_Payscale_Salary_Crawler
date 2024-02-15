import re
import json
import scrapy
from bs4 import BeautifulSoup
from furl import furl


class PayscaleSpider(scrapy.Spider):
    name = 'payscale'

    def start_requests(self):
        urls = [
            'https://www.payscale.com/research/SG/Industry'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_categories)


    def parse_categories(self, response):
        url = furl(response.request.url)
        parsed_html = BeautifulSoup(response.body, 'lxml')
        links = parsed_html.find_all('a', href=True)
        for a in links:
            if "research/SG/Industry/" in a["href"]:
                yield scrapy.Request(
                    url=f"https://{url.host}{a['href']}",
                    callback=self.parse_industries,
                    # pass down the category
                    cb_kwargs={
                        "category": a.text
                    }
                )


    def parse_industries(self, response, category):
        url = furl(response.request.url)
        parsed_html = BeautifulSoup(response.body, 'lxml')
        links = parsed_html.find_all('a', href=True)
        for a in links:
            if re.findall(r"research/SG/Industry=.*/Salary", a["href"]):
                yield scrapy.Request(
                    url=f"https://{url.host}{a['href']}",
                    callback=self.parse_salary,
                    # pass down category & industry
                    cb_kwargs={
                        "category": category,
                        "industry": a.text
                    }
                )


    def parse_salary(self, response, category, industry):
        parsed_html = BeautifulSoup(response.body, 'lxml')
        salary = parsed_html.select_one("span[class='default-overview__value']")
        # print(category, industry, salary.text)
        category = category.replace("/", " or ")
        industry = industry.replace("/", " or ")
        with open(f"payscaleSpiderResult/{category}_{industry}.json", 'w') as f:
            json.dump({
                "category": category,
                "industry": industry,
                "salary": salary.text
            }, f, indent=4)
