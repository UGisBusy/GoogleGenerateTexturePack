from GoogleCrawler import GoogleCrawler
from Processor import Processor

def test1():
    crawler = GoogleCrawler()
    processor = Processor()
    
    crawler.crawl_all()
    processor.process_all()

def clean():
    crawler = GoogleCrawler()
    processor = Processor()
    crawler.clean_raw_images_path()
    processor.clean_buffer_path()
    
if(__name__=='__main__'):
    test1()