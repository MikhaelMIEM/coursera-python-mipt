import requests
from multiprocessing.dummy import Pool as ThreadPool
import asyncio
import time
import sys


urls = ['http://ip-api.com/json/',
        'https://api.ipify.org/?format=json',
        'http://api.ipapi.com/31.207.234.252?access_key=7851660cf652f1c80547d085ffb16522',
        'https://api.myip.com/'
        ]


def sync_get():
    start = time.monotonic()
    sync_results = []
    for url in urls:
        sync_results.append(requests.get(url))
    end = time.monotonic()
    print('Sync: ', end - start, ' sec')

def threads_get():
    start = time.monotonic()
    pool = ThreadPool(4)
    threads_results = pool.map(requests.get, urls)
    pool.close()
    pool.join()
    end = time.monotonic()
    print('Threads: ', end - start, ' sec')


def asyncio_get():
    start = time.monotonic()
    async def async_get(url, loop):
        future = loop.run_in_executor(None, requests.get, url)
        data = await future
        return data

    loop = asyncio.get_event_loop()
    asyncio_results = loop.run_until_complete(asyncio.gather(*[async_get(url, loop) for url in urls]))
    loop.close()
    end = time.monotonic()
    print('Asyncio: ', end - start, ' sec')


if __name__ == '__main__':
    if sys.argv[1] == 's':
        sync_get()
    elif sys.argv[1] == 't':
        threads_get()
    elif sys.argv[1] == 'a':
        asyncio_get()
    else:
        pass

