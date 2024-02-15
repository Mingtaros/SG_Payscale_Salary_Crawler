# SG_Payscale_Salary_Crawler
Simply to crawl Yearly Salary from [Payscale](www.payscale.com) for SG Data.

# Running Steps
1. Install necessary requirements
    - `Scrapy==2.11.1`
    - `furl==2.1.3`
    - `beautifulsoup4==4.12.3`
2. Run the crawler `scrapy crawl payscale`.
3. If successful, it will save the result in `payscaleSpiderResult` directory
4. Run the converter script with `python conv_csv.py`
    - if `python` in local refers to Python 2, run with `python3`.
5. If successful, it will save the csv in `CategoryIndustrySalary.csv`.

# Special Thanks
1. [Payscale](www.payscale.com) for the data.
2. My group project members:
    - Choy Yu Min Justin
    - Daniel James
    - Laxmi Samhita Gade
    - Sei Sar Hla Kyi
