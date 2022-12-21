import shutil
from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler
import os

class Crawler:

    def __init__(self, types = []):
        self.raw_floder_path = 'raw_images'
        self.names_floder_path = 'names'
        self.types = types
        self.keyword_dict = dict()
        self.num = 1
    
    # clean the target floder before crawling
    def init_dir(self):
        if(os.path.exists(self.raw_floder_path)):
            shutil.rmtree(f'{self.raw_floder_path}')
        os.mkdir(self.raw_floder_path)
        for type in self.types:
            os.mkdir(f'{self.raw_floder_path}/{type}')

    # get names
    def get_keyword(self):
        for type in self.types:
            name_file = f'{self.names_floder_path}/{type}_names.txt'
            self.keyword_dict[type] = []
            with open(name_file, 'r') as f:
                for line in f.readlines():
                    self.keyword_dict[type].append(line.strip().replace('_', ' ')[:-4])

    # crawl images of certain type 
    def crawl_images(self, type):
        floder = f'{self.raw_floder_path}/{type}'
        crawler = CustomGoogleImageCrawler(storage={'root_dir': floder}, downloader_cls=CustomDownloader)
        for k in self.keyword_dict[type]:
            crawler.crawl(keyword=k, max_num=self.num)
            
    

# change the downloader to accept the keyword
class CustomDownloader(ImageDownloader):
    def get_filename(self, task, default_ext, keyword):
        return f'{keyword.replace(" ", "_")}.{default_ext}'

    def keep_file(self, task, response, min_size=None, max_size=None, **kwargs):
        # normally, this will comapre the size of the image with min_size and max_size,
        # but we don't need it, so we just return True
        return True

    def download(self, task, default_ext, timeout=5, max_retry=3, overwrite=False, **kwargs):
        """Download the image and save it to the corresponding path.
        Args:
            task (dict): The task dict got from ``task_queue``.
            timeout (int): Timeout of making requests for downloading images.
            max_retry (int): the max retry times if the request fails.
            **kwargs: reserved arguments for overriding.
        """
        file_url = task['file_url']
        task['success'] = False
        task['filename'] = None
        retry = max_retry
        keyword = kwargs['keyword']

        if not overwrite:
            with self.lock:
                self.fetched_num += 1
                filename = self.get_filename(task, default_ext,keyword)
                if self.storage.exists(filename):
                    self.logger.info('skip downloading file %s', filename)
                    return
                self.fetched_num -= 1

        while retry > 0 and not self.signal.get('reach_max_num'):
            try:
                response = self.session.get(file_url, timeout=timeout)
            except Exception as e:
                self.logger.error('Exception caught when downloading file %s, '
                                  'error: %s, remaining retry times: %d',
                                  file_url, e, retry - 1)
            else:
                if self.reach_max_num():
                    self.signal.set(reach_max_num=True)
                    break
                elif response.status_code != 200:
                    self.logger.error('Response status code %d, file %s',
                                      response.status_code, file_url)
                    break
                elif not self.keep_file(task, response, **kwargs):
                    break
                with self.lock:
                    self.fetched_num += 1
                    filename = self.get_filename(task, default_ext,keyword)
                self.logger.info('image #%s\t%s', self.fetched_num, file_url)
                self.storage.write(filename, response.content)
                task['success'] = True
                task['filename'] = filename
                break
            finally:
                retry -= 1

# need to override the crawl method to pass the keyword to the downloader
class CustomGoogleImageCrawler(GoogleImageCrawler):
    def crawl(self, keyword, filters=None, offset=0, max_num=1000, min_size=None, max_size=None, language=None, file_idx_offset=0, overwrite=False):
        feeder_kwargs = dict(
            keyword=keyword,
            offset=offset,
            max_num=max_num,
            language=language,
            filters=filters)
        downloader_kwargs = dict(
            keyword=keyword,  # <<< add this line
            max_num=max_num,
            min_size=min_size,
            max_size=max_size,
            file_idx_offset=file_idx_offset,
            overwrite=overwrite)
        super(GoogleImageCrawler, self).crawl(
            feeder_kwargs=feeder_kwargs, downloader_kwargs=downloader_kwargs)
