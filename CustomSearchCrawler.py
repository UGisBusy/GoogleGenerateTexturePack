import requests
import urllib.request
from Crawler import Crawler

class CustomSearchCrawler(Crawler):
    __api_key = 'YOUR API KEY'
    __engine_id = 'YOUR ENGINE ID'

    def crawl_images(self, type):
        for k in self.keyword_dict[type]:
            # print(f'searching {k}')
            # url = f'https://www.googleapis.com/customsearch/v1?key={self.__api_key}&cx={self.__engine_id}&q={k}&searchType=image&num=1&start={offset}'
            url = f'https://www.googleapis.com/customsearch/v1/siterestrict?key={self.__api_key}&cx={self.__engine_id}&q={k}&searchType=image&num=1'
            data = requests.get(url).json()
            
            if('error' in data):
                print(f'error message: {data["error"]["message"]}')
                break
            if(data['searchInformation']['totalResults'] == '0'):
                print(f'fail to find {k}')
                continue
            img_link = data['items'][0]['link']
            try:
                urllib.request.urlretrieve(img_link, f'{self.raw_images_path}/{type}/{k.replace(" ", "_")}.png')
            except:
                print(f'fail to find {k}')
            