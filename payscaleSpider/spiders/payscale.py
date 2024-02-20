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
        # data can be found on __NEXT_DATA__ script
        json_data = parsed_html.select_one("script[id='__NEXT_DATA__']")
        parsed_json = json.loads(json_data.text)
        job_salaries = parsed_json["props"]["pageProps"]["pageData"]["byDimension"]
        if job_salaries == None:
            return

        job_salaries = job_salaries["Average Salary by Job"]["rows"]
        
        category = category.replace("/", " or ")
        industry = industry.replace("/", " or ")
        salary_obj = []
        for job_salary in job_salaries:
            for quantile in job_salary["range"]:
                salary_obj.append({
                    "category": category,
                    "industry": industry,
                    "job_title": job_salary["name"],
                    "quantile": quantile,
                    "salary": job_salary["range"][quantile]
                })
        
        with open(f"payscaleSpiderResult/{category}_{industry}.json", 'w') as f:
            json.dump(salary_obj, f, indent=4)
