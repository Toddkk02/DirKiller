import os
import contextlib
import queue
from urllib import request
import sys
import threading
from termcolor import colored
from tqdm import tqdm
import argparse
import curses

# Creazione del parser per gli argomenti da riga di comando
argparser = argparse.ArgumentParser(description='Yep another dirBuster')
argparser.add_argument('-u', "--url", help='The target domain to scan (www.example.com)', required=True)
argparser.add_argument('-w', "--wordlist", help='The path to the wordlist', required=True)
argparser.add_argument('-t', '--threads', type=int, default=25, help='Number of threads to use')

# Parsing degli argomenti
args = argparser.parse_args()

# Assegnazione dei parametri
TARGET = args.url.rstrip('/')  # Rimuove eventuali slash finali
FILTERED = [".jpg", ".png", ".gif", ".css"]
THREADS = args.threads

answers = queue.Queue()
web_path = queue.Queue()

def gather_paths():
    wordlist = args.wordlist  # Otteniamo il percorso della wordlist
    if not os.path.exists(wordlist):
        print(colored(f"Error: {wordlist} does not exist!", "red"))
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

def test_remote(progress_bar, stdscr, start_row):
    row = start_row  # Start printing results after the header
    while not web_path.empty():
        path = web_path.get()
        url = f"https://{TARGET}/{path}"
        try:
            r = request.urlopen(url)
            if r.status == 200:
                result = f"{url} is accessible"
                stdscr.addstr(row, 0, colored(result, "green"))
            else:
                result = f"{url} returned status {r.status}"
                stdscr.addstr(row, 0, colored(result, "blue"))
            answers.put(r.status)
        except Exception as e:
            result = f"{url} failed"
            stdscr.addstr(row, 0, colored(result, "red"))
            answers.put(None)
        
        stdscr.refresh()
        row += 1
        web_path.task_done()
        progress_bar.update(1)

def run(stdscr):
    threads = []
    total_paths = web_path.qsize()  # Ottieni il numero totale di percorsi dalla wordlist
    # Imposta la posizione del cursore alla parte superiore dello schermo
    start_row = 2  # Partiamo dalla riga 2 per lasciare spazio alla barra di progresso
    with tqdm(total=total_paths, desc="Scanning", unit="path", position=0, ncols=100) as progress_bar:
        for _ in range(THREADS):
            t = threading.Thread(target=test_remote, args=(progress_bar, stdscr, start_row))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

def main(stdscr):
    # Setup iniziale del terminale
    curses.curs_set(0)  # Nasconde il cursore
    stdscr.nodelay(1)  # Impedisce che il terminale aspetti un input

    gather_paths()

    # Imposta la finestra di terminale per il testo in tempo reale
    stdscr.clear()
    stdscr.addstr(0, 0, "Starting scan...\n")
    stdscr.refresh()

    run(stdscr)
    
    # Ora stampiamo i risultati dopo che la scansione è terminata
    while not answers.empty():
        status_code = answers.get()
        if status_code:
            stdscr.addstr(0, 0, f"HTTP status code: {status_code}\n", curses.A_BOLD)
            stdscr.refresh()

    stdscr.addstr(0, 0, colored("Finished scanning.", "cyan") + "\n")
    stdscr.refresh()
    stdscr.getch()  # Aspetta un input per chiudere

if __name__ == "__main__":
    curses.wrapper(main)
