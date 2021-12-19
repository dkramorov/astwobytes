import requests
import queue
import threading


"""
concurrent = 200

def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print status, url

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in open('urllist.txt'):
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
"""

product_links = ["https://www.rupool.ru/good/490260", "https://www.rupool.ru/good/490261", "https://www.rupool.ru/good/490262", "https://www.rupool.ru/good/490263", "https://www.rupool.ru/good/286120", "https://www.rupool.ru/good/286121", "https://www.rupool.ru/good/286118", "https://www.rupool.ru/good/286119", "https://www.rupool.ru/good/286116", "https://www.rupool.ru/good/286117", "https://www.rupool.ru/good/286114", "https://www.rupool.ru/good/286115", "https://www.rupool.ru/good/286112", "https://www.rupool.ru/good/286113", "https://www.rupool.ru/good/286110", "https://www.rupool.ru/good/286111", "https://www.rupool.ru/good/365750", "https://www.rupool.ru/good/365751", "https://www.rupool.ru/good/372531", "https://www.rupool.ru/good/372532", "https://www.rupool.ru/good/372533", "https://www.rupool.ru/good/372534"]


concurrent = 200

def do_work():
    while True:
        url = q.get()
        r = get_url(url)
        analyze_result(r)
        q.task_done()

def get_url(ourl):
    try:
        r = requests.get(url)
        return r
    except Exception as e:
        print(e)
    return None

def analyze_result(r):
    print(r.status_code, r.request.url)


class ParallelRequests:
    def __init__(self):
        self.concurrent = 200
        self.q = queue.Queue(self.concurrent * 2)

    def do_work(self):
        while True:
            url = self.q.get()
            r = self.get_url(url)
            self.analyze_result(r)
            self.q.task_done()

    def get_url(self, url):
        try:
            r = requests.get(url)
            return r
        except Exception as e:
            print(e)
        return None

    def analyze_result(self, r):
        print(r.request.url, r.status_code)

    def tasker(self, links):
        for i in range(self.concurrent):
            t = threading.Thread(target=self.do_work)
            t.daemon = True
            t.start()
        for url in links:
            self.q.put(url)
        self.q.join()

pr = ParallelRequests()
pr.tasker(product_links)

exit()

q = queue.Queue(concurrent * 2)
for i in range(concurrent):
    t = threading.Thread(target=do_work)
    t.daemon = True
    t.start()
try:
    for url in product_links:
        q.put(url)
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
