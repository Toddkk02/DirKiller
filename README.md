# Web Directory Scanner (Mapper)

This is a simple tool for performing directory busting (directory scanning) on a website, similar to **dirBuster** and **gobuster**. It uses a wordlist to search for directories or files on a web server, testing their accessibility via HTTP requests.

## Features

- Performs directory scanning on a website using a wordlist.
- Supports parallel execution through multithreading for faster scanning.
- Displays the HTTP status for each tested URL (200, 404, etc.).
- Dynamic progress bar using `tqdm`.
- Results are printed above the progress bar to avoid overlapping with dynamic output.

## Prerequisites

To run the program, you need Python 3.x installed along with the following Python libraries:

- `tqdm` – For the progress bar.
- `termcolor` – For coloring the text output.
- `curses` – For managing dynamic terminal interface.

You can install the required packages with `pip`:

```bash
pip install tqdm termcolor

Note: curses is built-in with Python on Unix-based systems, so you don’t need to install it separately on Linux or macOS. On Windows, an additional module like windows-curses is required.
Usage
Running the Program

To run the program, use the following command:

python3 mapper.py -u <URL_TARGET> -w <WORDLIST_PATH> -t <THREADS>

Arguments:

    -u, --url : The target website URL (e.g., www.example.com).
    -w, --wordlist : The path to the wordlist file (e.g., /path/to/wordlist.txt).
    -t, --threads : Number of threads to use for the scan. The default value is 25.

Example:

python3 mapper.py -u www.example.com -w /path/to/wordlist.txt -t 25

Output:

The program will progressively show the scanning progress and the results for each URL tested:

    Green: URL is accessible (HTTP status 200).
    Blue: URL returned a status different from 200.
    Red: URL failed the connection or returned an error.

Once the scan is complete, the program will show a final message with the completion of the scan and the status of each tested URL.
Example Output

Starting scan...
Scanning: 100%|██████████| 200/200 [00:02<00:00, 98.53path/s]

https://www.example.com/path/to/resource is accessible
https://www.example.com/another/path returned status 404
Finished scanning.

How it Works

    Loading the Wordlist: The program loads the wordlist file from which it generates paths to test.
    HTTP Testing: For each generated path, an HTTP request is made to check its accessibility.
    Multithreading: To speed up the process, the program uses multiple threads to test several URLs simultaneously.
    Dynamic Display: The progress bar is updated in real-time, showing the scanning progress. Results are printed above the progress bar without overlapping.

Contributing

If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.
License

This program is released under the MIT license. See the LICENSE file for details.

 
