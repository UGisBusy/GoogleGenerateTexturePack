import requests, lxml, re, json, urllib
from bs4 import BeautifulSoup
from Crawler import Crawler

class BeautifulCrawler(Crawler):

    def crawl_images(self, type):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
        params = {
            'q': 'keyword', # search query
            'tbm': 'isch',  # image results
            'hl': 'en',     # language of the search
            'gl': 'us',     # country where search comes from
        }
        
        for k in self.keyword_dict[type]:
            params['q'] = k
            html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
            soup = BeautifulSoup(html.text, "lxml")
    
            # get the image data
            script_tags_data = soup.select('script')
            
            data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(script_tags_data)))
            data_json = json.loads(json.dumps(data))
            google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', data_json)
    
            # extract the thumbnails urls
            google_images_thumbnails = ", ".join(re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', str(google_image_data))).split(", ")
            thumbnails = [bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in google_images_thumbnails]

            # extract the full resolution images urls
            removed_matched_google_images_thumbnails = re.sub(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(google_image_data))
            google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)
            full_resolution_images = [bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in google_full_resolution_images]

            # download the full res image 
            for id,url in enumerate(full_resolution_images):
                try:
                    print(f'keyword:{k} >> ', end='')
                    if(requests.get(url, timeout=1, stream=True).status_code != 200):
                        print('request denied, try next')
                        print(f'url:{url}')
                        continue
                    urllib.request.urlretrieve(url, f'{self.raw_images_path}/{type}/{k.replace(" ", "_")}.png')
                    print('success')
                    break
                except:
                    print('failed, try next')
                    pass
            else:
                print(f'fail to find {k}')
