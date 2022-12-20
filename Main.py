from Crawler import Crawler
from Processor import Processor

def test1():
    crawler = Crawler(types=['block'])
    crawler.init_dir()
    crawler.get_keyword()
    crawler.crawl_images('block')

    processor = Processor(size=16)
    processor.init_dir()
    processor.process('block')

def clean():
    crawler = Crawler(types=['block'])
    crawler.init_dir()
    processor = Processor(size=16)
    processor.init_dir()

if(__name__=='__main__'):
    clean()