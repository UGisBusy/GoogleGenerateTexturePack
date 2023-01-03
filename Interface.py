import tkinter
from ICrawler import ICrawler
from CustomSearchCrawler import CustomSearchCrawler
from BeautifulCrawler import BeautifulCrawler
from UnsplashCrawler import UnsplashCrawler
from Processor import Processor

class Interface():

    def __init__(self, resolution, types):
        self.resolution = resolution
        self.types = types
    def start(self):
        def gen():
            which_resolution = radio_v_resolution.get()
            which_source = radio_v_source.get()
            which_type = radio_v_types.get()
            crawler_dict = {0: CustomSearchCrawler, 1: UnsplashCrawler, 2: ICrawler, 3: BeautifulCrawler}
            type_dict = {0: ['block'], 1: ['nature_block']}
            crawler = crawler_dict[which_source](types=type_dict[which_type])
            processor = Processor(resolution=resolution_v[which_resolution], types=type_dict[which_type], result_path=raw_images_path.get())
            
            crawler.crawl_all()
            processor.process_all()
        def clean():
            crawler = CustomSearchCrawler()
            processor = Processor()
            crawler.clean_raw_images_path()
            processor.clean_buffer_path()

        win = tkinter.Tk()
        win.title('Crawler')
        win.geometry('500x500')
        btn_gen = tkinter.Button(win, text='Generate', command=gen)
        btn_clean = tkinter.Button(win, text='Clean', command=clean)
        label_file = tkinter.Label(win, text='File location:', fg='blue') 
        raw_images_path = tkinter.StringVar()
        entry_path = tkinter.Entry(win, width=20, textvariable=raw_images_path)
        label_resolution = tkinter.Label(win, text='Image resolution:', fg='blue')
        resolution = self.resolution
        resolution_v = [int(i.split('x')[0]) for i in list(resolution.values())]
        radio_v_resolution = tkinter.IntVar()
        radio_v_resolution.set(0)
        for i in range(len(resolution)):
            tkinter.Radiobutton(win, text=resolution[i], variable=radio_v_resolution, value=i).grid(row=3+i , column=0, sticky='w')
        label_source = tkinter.Label(win, text='Image source:', fg='blue')
        source = {0: 'Custom Search Crawler', 1: 'Unsplash Crawler', 2: 'ICrawler', 3: 'Beautiful Crawler'} 
        radio_v_source = tkinter.IntVar()
        radio_v_source.set(0)
        for i in range(len(source)):
            tkinter.Radiobutton(win, text=source[i], variable=radio_v_source, value=i).grid(row=7+i , column=0, sticky='w')
        label_types = tkinter.Label(win, text='Types:', fg='blue')
        types = self.types
        radio_v_types = tkinter.IntVar()
        radio_v_types.set(0)
        for i in range(len(types)):
            tkinter.Radiobutton(win, text=types[i], variable=radio_v_types, value=i).grid(row=12+i , column=0, sticky='w')

        label_file.grid(row=0, column=0, sticky='w')
        entry_path.grid(row=1, column=0, sticky='w')
        label_resolution.grid(row=2, column=0, sticky='w')
        label_source.grid(row=6, column=0, sticky='w')
        label_types.grid(row=11, column=0, sticky='w')
        btn_gen.grid(row=3, column=8)
        btn_clean.grid(row=5, column=8)
        win.mainloop()
