import csv
from multiprocessing.dummy import Pool
import threading
import queue

cores = 16
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


def determine(site):
    url = site[0]
    cond = url.find('.dk/') != -1
    seen.put((cond, url))


def main():
    threading.Thread(target=loop, daemon=True).start()

    csv_file = open('../shopify.csv', 'r')
    csv_iter = csv.reader(csv_file, delimiter=';')
    pool.map(determine, csv_iter)


if __name__ == '__main__':
    main()
