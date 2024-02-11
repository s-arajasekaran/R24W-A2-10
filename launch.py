from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
from scraper import getStats


def main(config_file, restart):
    longestPage =  ("", 0)
    allWords= {}
    hist = []
    uniqueList = set()
    subDomainList = {}
    metaData = (longestPage, allWords, hist, uniqueList, subDomainList)
    
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart, md = metaData)
    try:
        crawler.start()
        getStats(crawler.metaData)
    except:
        getStats(crawler.metaData)
    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
