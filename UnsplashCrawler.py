from bs4 import BeautifulSoup
import requests, urllib.request
# from tqdm import tqdm 可看進度條
from time import sleep
from Crawler import Crawler


class UnsplashCrawler(Crawler):
    def crawl_images(self, type):

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        folder = f'{self.raw_images_path}/{type}'

        for line in self.keyword_dict[type]:
            #   query = line
            #   image_title = line
            #   endpage = 1

            # query
            # query = input('Enter your keyword:')
            query = line

            # endpage = int(input('How many pages do you want to scrap:'))
            endpage = 1

            # per_page=10  ->  1 page search 10 pic    ===> 10
            api_url = ['https://unsplash.com/napi/search/photos?query={}&per_page=10&page={}&xp='.format(query, x) for x in range(0, endpage)]

            success = 0

            for url in api_url:                             # tqdm(api_url) 可看進度條
                # print('\n------------------------\n')
                # sent requests to server
                r = requests.get(url, headers=headers)
                json_daata = r.json()
                
                for image in json_daata['results']:         # tqdm(json_daata['results']) 可看進度條
                    # print('\n-----------img-------------\n')
                    image_title = query.replace(" ", "_")   # image['alt_description'] 變成下載的圖片的名稱
                    image_url = image['urls']['raw']
                    
                    # write image files
                    try:
                        urllib.request.urlretrieve(image_url, folder + '/' + image_title + '.png')
                        # with open(folder + '/' + image_title + '.png', 'wb') as File:
                        #     r = requests.get(image_url, stream=True)
                        #     File.write(r.content)
                        #     print("\n" + image_title + " success")
                        success = 1
                    except:
                        pass

                    if success == 1:
                        break
                if success == 1:
                    # print("end download")
                    break

            if success == 0:
                ok = 0

                print("\n{} fail".format(query))
                print("try to find i stock :")
                input_image = query
                
                response = requests.get(f"https://unsplash.com/s/photos/{input_image}")
                soup = BeautifulSoup(response.text, "lxml")
                
                resultsWithSoup = soup.find_all("img", {"class": "tB6UZ a5VGX"}, limit=1)
                
                image_links = [result.get("src") for result in resultsWithSoup]  # 取得圖片來源連結
                
                for link in image_links:
                    try:
                        img_download = requests.get(link)  # 下載圖片
                        image_title = query.replace(" ", "_")
                        with open(folder + '/' + image_title + ".png", "wb") as file:  # 開啟資料夾及命名圖片檔
                            file.write(img_download.content)  # 寫入圖片的二進位碼
                            print("i stock:\n" + image_title + " success\nend i stock")
                            ok = 1
                    except:
                        pass

                    #sleep(1)
                    if ok == 1:
                        break
                
                if ok == 0:
                    print(image_title + " fail :(")