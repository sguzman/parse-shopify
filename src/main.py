import csv
from multiprocessing.dummy import Pool
import threading
import queue
import random
import requests
import bs4
import sys
import asyncio

cores = 4
pool = Pool(cores)
seen = queue.Queue()


def loop():
    global cores

    idx = 0
    while True:
        cond, msg = seen.get(block=True)
        if cond:
            idx += 1
            print(idx, msg)
        print(msg)


async def retrieve(site):
    try:
        url = site[0]
        cond = url.find('.dk/') != -1
        text = requests.get(url).text
        soup = bs4.BeautifulSoup(text, 'html.parser')
        html = soup.select_one('html[lang]')
        if html is None:
            lang = None
        else:
            lang = html['lang']

        seen.put((cond, [url, lang]))
    except Exception as e:
        print(e, file=sys.stderr)


def determine(site):
    asyncio.run(retrieve(site))


def main():
    threading.Thread(target=loop, daemon=True).start()

    csv_file = open('../shopify.csv', 'r')
    csv_iter = list(csv.reader(csv_file, delimiter=';'))
    random.shuffle(csv_iter)

    pool.map(determine, csv_iter)


if __name__ == '__main__':
    main()
