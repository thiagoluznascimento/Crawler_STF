import sys

from src.crawler import CrawlerStf
# python3 run.py "2022-12-14"
data = sys.argv[1]
CrawlerStf(data).baixa_cadernos()
