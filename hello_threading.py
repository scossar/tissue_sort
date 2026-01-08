import threading
import time


def crawl(link, delay=3):
    print(f"crawl started for {link}")
    time.sleep(delay)
    print(f"crawl ended for {link}")


links = [
    "https://zalgorithm.com",
    "https://zalgorithm.com/notes",
    "https://zalgorithm.com/tags",
]

threads = []
for link in links:
    # using `args` to pass positional args and `kwards` for keyword args
    t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
