from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import time
import tkinter as tk
import threading
website = "http://www.galnote.com"
downloadpath = ""
imageSequence = 0
mode = "wallpaper" # illustration wallpaper comicstrip
prename = "" 
start = 1
end = 6

num = 0

win = tk.Tk()
win.title("galget")


def geturl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), features="html.parser")
    except AttributeError as e:
        return None
    
    return bsObj

def retrieveFromImagePage(url, prename, pre):
    global imageSequence, downloadpath, win, num
    
    if "http" not in url:
        url = website + url
    imagePage = geturl(url)
    if imagePage == None:
        print("Error ImagePage")
        exit(-1)
    imagelocation =website+imagePage.find("div", {"class": "d-flex flex-row bd-highlight"}).\
    find("div", {"class": "bd-highlight"}).find("a")["href"]
    suffix = imagelocation[imagelocation.rindex('.'):]
    if downloadpath[-1] != '/' and downloadpath[-1] != '\\':
        downloadpath += '/'
    urlretrieve(imagelocation, f"{downloadpath}{prename}{pre}_{imageSequence}"+suffix)
    imageSequence += 1
    num += 1
    print(f"已下载{num}张图片")
    win.title(f"{num} pictures downloaded!")
    

def get(mode, start, end, prename):
    global win
    for i in range(start, end+1):
        global imageSequence
        imageSequence = 0
        
        pagenum = i
        root = geturl(f"{website}/post/by?ct={mode}&page={pagenum}")
        if root == None:
            print("Error Get Root Page")
            exit(-1)

        pages = root.find_all("a", {"class": "a-img", "rel": "noopener"})
        timestr = str(time.process_time())[2:6]
        for page in pages:
            retrieveFromImagePage(page["href"], prename, timestr)
    print("\n\nall pictures downloaded")
    win.title("galget")

tk.Label(win, text="请选择分类: ").grid(row=0, columnspan=3)
modVar = tk.StringVar()
modVar.set("illustration")
tk.Radiobutton(win, text="插画", variable=modVar, value="illustration").grid(row=1, column=0)
tk.Radiobutton(win, text="壁纸", variable=modVar, value="wallpaper").grid(row=1, column=1)
tk.Radiobutton(win, text="四格漫画", variable=modVar, value="comicstrip").grid(row=1, column=2)
tk.Label(win, text="请输入下载范围(单位是页, 一页12张): ").grid(row=2, columnspan=3)
sInp = tk.Entry(win)
sInp.grid(row=3, column=0)
tk.Label(win, text="到").grid(row=3, column=1)
eInp = tk.Entry(win)
eInp.grid(row=3, column=2)
tk.Label(win, text="请输入下载路径(默认下载到当前路径): ").grid(row=4, columnspan=3)
txtVar = tk.StringVar()
txtVar.set("./")
inp = tk.Entry(win, textvariable=txtVar)
inp.grid(row=5, columnspan=3)

def down():
    global downloadpath
    print("start downloading")
    win.title("开始下载")
    downloadpath = inp.get()  
    get(modVar.get(), int(sInp.get()), int(eInp.get()), 'setu')

tk.Button(win, text="下载", command=threading.Thread(target=down).start).grid(row=6, columnspan=3)

win.mainloop()