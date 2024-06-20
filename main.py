import argparse
import threading
import time
from urllib.request import urlopen
from multiprocessing import Process
import asyncio
import aiohttp


counter = 0
lock = threading.Lock()

def download(url):
    start_time = time.time()  
    global counter
    response = urlopen(url)
    file_name = 'data/'+url.replace('https://','').replace('.','_').replace('/','')+ '.jpg'
    with open(file_name, 'wb') as f:
        f.write(response.read())
    with lock:
            counter += time.time() - start_time
    print(f'dowloading: {url} in {time.time() - start_time:.2f} seconds')
    print(f'общее время выполнения скачивания: {counter:.2f}') 


def multiprocess(urls):
    processes = []
    for url in urls:
        prosess = Process(target= download, args=(url,))
        processes.append(prosess)
        prosess.start()

    for prosess in processes:
        prosess.join()   





def thread_(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target= download, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  



async def dowload_asin(url):
    global counter
    start_time = time.time()  
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.read()  


    filename = 'data/asyncio_'+ url.replace('https://','').replace('.','_').replace('/','')+ '.jpg'   
    with open(filename,'wb') as f:
        f.write(img)
        counter += time.time() - start_time
    print(f'Downloaded {url} in {time.time() - start_time:.2f} seconds') 
    print(f'общее время выполнения скачивания: {counter:.2f}') 


async def main_asin(urls):
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(dowload_asin(url))
        tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='парсер изображений по url')
    parser.add_argument('--urls', nargs='+', help='список адресов')
    args = parser.parse_args() 
    urls = args.urls

    print(f'загрузка потоки') 
    thread_(urls)

    print(f'загрузка мультипроцессы')
    multiprocess(urls) 

    print(f'загрузка  асинхронно')
    main_asin(urls)
