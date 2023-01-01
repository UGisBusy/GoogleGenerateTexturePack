from ICrawler import ICrawler
from CustomSearchCrawler import CustomSearchCrawler
from BeautifulCrawler import BeautifulCrawler
from UnsplashCrawler import UnsplashCrawler
from Processor import Processor

def test():

    crawler_dict = {0: CustomSearchCrawler, 1: UnsplashCrawler, 2: ICrawler, 3: BeautifulCrawler}
    type_dict = {0: ['block'], 1: ['nature_block']}
    
    which_crawler = 3
    which_type = 1

    crawler = crawler_dict[which_crawler](types=type_dict[which_type])
    processor = Processor(types=['nature_block'], result_path='C:\\Users\\user\\Desktop\\playground\\python\\GoogleGenerateTexturePack\\texturepack')
    
    crawler.crawl_all()
    processor.process_all()

def clean():
    crawler = CustomSearchCrawler()
    processor = Processor()
    crawler.clean_raw_images_path()
    processor.clean_buffer_path()
    
if(__name__=='__main__'):
    test()