#!/usr/bin/env python3

from bs4 import BeautifulSoup
from argparse import ArgumentParser
from threading import Thread
from sys import stdin
from modules.request import *
from modules.headless import *
from modules.html_function import *
from modules.json_function import *
from modules.xml_function import *
from modules.sitemap_params import *
from modules.banner import *

# Arguments
parser = ArgumentParser(add_help=False)
parser.add_argument('-u', '--url', nargs='?', type=str, default='', help='Provide an URL to get params. (To single URL check) - e.g. -d/--domain "domain.tld/path1/path2/path3"')
parser.add_argument('-l', '--list', nargs='?', type=str, default='', help="Domain list file. (To multiple URL check) - e.g. -l/--list domains.txt")
parser.add_argument('-f', '--file', nargs='?', type=str, default='', help="HTTP request response file - e.g. -f/--file response.txt")
parser.add_argument('-s', '--silent', help="Silent mode", action="store_true")
parser.add_argument('-x', '--exclude', type=str, default='', help="Exclude content-type - e.g. -x/--exclude json,xml")
parser.add_argument('-o', '--output', type=str, default='', help="Output <string> - e.g. output.txt")
parser.add_argument('-t', '--thread', type=int, default='2', help="Thread <int> - default: 2")
parser.add_argument('-hl', '--headless', type=str, default='', help="Send request in headless mode - e.g. -hl/--headless chrome")
parser.add_argument('-dp', '--driver_path', type=str, default='', help="Full path to the browser driver to use - e.g. -hl/--headless chrome -dp/--driver_path /path/to/chromedriver")
parser.add_argument('-nl', '--no_logging', help="Running the tool without saving logs, logs are saved by default", action="store_true")
parser.add_argument('-ru', '--random_useragent', help="Random User-Agent", action="store_true")
parser.add_argument('-h', '--help', action='store_true', help='Display help message')

args = parser.parse_args()

# Logging
if not args.no_logging:
    import logging
    logging.basicConfig(filename="log", format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

class colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NOCOLOR = '\033[0m'

if not args.silent:
    banner(colors)


if args.help:
    parser.print_help()

# Crawling function
def crawling(url):
    try:
        # request functions
        if args.headless:
            response = headless_function(args, url)
        else:
            response = request_function(args, url)

        content_type = response.headers.get('content-type')

        if args.exclude:
            exclude = args.exclude.replace(' ', '').split(',')
        else:
            exclude = []

        # Check if content-type is JSON
        if 'application/json' in content_type and not 'json' in exclude:
            params = json_params(response)

        # Check if content-type is XML
        elif 'application/xml' in content_type and not 'xml' in exclude:
            params = xml_params(response)
        # Crawl HTML
        else:
            params = html_crawling(response.text, url, logger, args)
            

        # Output
        if args.output == '':
            if not args.silent == '':
                print()
                print()
                print(url)
                print('==========================================================')
                
            for param in params:
                print(param)
        else:
            if not args.silent == '':
                print()
                print()
                print(url)
                print('==========================================================')

            for param in params:
                print(param)
                with open(args.output, 'a') as f:
                    f.write(param+'\n')
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass
    else:
        pass
    
# Threading function
def thread(urls):
    chunk_size = len(urls) // int(args.thread)
    if chunk_size == 0:
        for url in urls:
            crawling(url)
        return

    chunks = [urls[i:i+chunk_size] for i in range(0, len(urls), chunk_size)]

    threads = []

    for chunk in chunks:
        thread = Thread(target=lambda urls: [crawling(url) for url in urls], args=(chunk,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


# Get a list of URLs
if args.list != '':
    urls = [line.strip() for line in open(args.list)]
    urls = list(set(urls))
    complete_urls = []
    for url in urls:
        if not url.startswith("http://") and not url.startswith("https://"):
            complete_urls.append("https://{}".format(url))
        else:
            complete_urls.append(url)
    try:
        thread(complete_urls)
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass

# Get single URL
elif args.url != '':
    url = args.url
    complete_urls = []
    if not url.startswith("http://") and not url.startswith("https://"):
        complete_urls.append("https://{}".format(url))
    else:
        complete_urls.append(url)

    try:
        thread(complete_urls)
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass

elif args.file != '':
    if not args.no_logging:
        params = sitemap(args, logger)
    else:
        params = sitemap(args)
    if args.output == '':
        for param in params:
            print(param)
    else:
        for param in params:
            print(param)
            with open(args.output, 'a') as f:
                f.write(param+'\n')

# Get input from pipeline stdin
else:
    if not stdin.isatty():
        input_urls = [line.strip() for line in stdin.readlines()]
        if len(input_urls) == 1:
            try:
                complete_urls = []

                url = input_urls[0]

                if ',' in url:
                    url = url.split(',')[0]

                if not url.startswith("http://") and not url.startswith("https://"):
                    complete_urls.append("https://{}".format(url))
                else:
                    complete_urls.append(url)

                thread(complete_urls)
            except Exception as e:
                if not args.no_logging:
                    logger.error(e)
                pass
        else:
            input_urls = list(set(input_urls))
            complete_urls = []
            for url in input_urls:
                if not url.startswith("http://") and not url.startswith("https://"):
                    complete_urls.append("https://{}".format(url))
                else:
                    complete_urls.append(url)
            try:
                thread(complete_urls)
            except Exception as e:
                if not args.no_logging:
                    logger.error(e)
                pass
    else:
        print()
        print(colors.RED + '[-] ' + colors.NOCOLOR + 'Provide an URL or a file')