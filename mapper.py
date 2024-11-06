import os
import contextlib
import queue
from urllib import request
import sys
import threading

FILTERED = [".jpg", ".png", ".gif", ".css"]
THREADS = 10

answers = queue.Queue()
web_path = queue.Queue()

def gather_paths():
    try:
        wordlist = sys.argv[2]  # Get the path of the wordlist
    except IndexError:
        print("Error: Wordlist required!")
        print("Usage: python3 mapper.py <target> <wordlist>")
        return
    if not os.path.exists(wordlist):
        print(f"Error: {wordlist} does not exist!")
        return
    with open(wordlist, 'r') as f:
        for word in f:
            path = word.strip()
            if not any(path.endswith(ext) for ext in FILTERED):
                web_path.put(path)
    return web_path

@contextlib.contextmanager
def chdir(path):
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

def test_remote():
    while not web_path.empty():
        path = web_path.get()
        url = f"https://{TARGET}/{path}"
        try:
            r = request.urlopen(url)
            if r.status == 200:
                sys.stdout.write(f"{url} is accessible\n")
            answers.put(r.status)
        except Exception as e:
            sys.stdout.write(f"Error accessing {url}: {e}\n")
            answers.put(None)
        sys.stdout.flush()
        web_path.task_done()

def run():
    threads = []
    print("Spawning threads...")
    for _ in range(THREADS):
        t = threading.Thread(target=test_remote)
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 mapper.py <target> <wordlist>")
        sys.exit(1)
    TARGET = sys.argv[1].rstrip('/')  # Ensure no trailing slash
    gather_paths()
    run()
    while not answers.empty():
        status_code = answers.get()
        if status_code:
            print(f"HTTP status code: {status_code}")
    print("Finished")
