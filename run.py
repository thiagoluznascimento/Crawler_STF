import sys

from src.crawler import CrawlerStf

data = sys.argv[1]
CrawlerStf(data).baixa_cadernos()
