#!/usr/bin/env python3

from bs4 import BeautifulSoup
from re import sub,findall
from argparse import ArgumentParser
from requests import Session
from requests import get as request_get
from threading import Thread
from json import loads as json_loads
from sys import stdin
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from random import choice

# Arguments
parser = ArgumentParser(add_help=False)
parser.add_argument('-d', '--domain', nargs='?', type=str, default='', help='Provide an URL to get params. (To single URL check) - e.g. -d/--domain "domain.tld"')
parser.add_argument('-l', '--list', nargs='?', type=str, default='', help="Provide a file to get params. (To multiple URL check) - e.g. -l/--list domains.txt")
parser.add_argument('-s', '--silent', help="Silent mode", action="store_true")
parser.add_argument('-x', '--exclude', type=str, default='', help="Exclude content-type - e.g. -x/--exclude json,xml")
parser.add_argument('-o', '--output', type=str, default='', help="Output <string> - e.g. output.txt")
parser.add_argument('-t', '--thread', type=int, default='1', help="Thread <int> - default: 1")
parser.add_argument('-nl', '--no_logging', help="Running the tool without saving logs, logs are saved by default", action="store_true")
parser.add_argument('-ru', '--random_useragent', help="Random User-Agent", action="store_true")
parser.add_argument('-h', '--help', action='store_true', help='display help message')

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
    print()                
    print()
    print("  __   _    _ _ ____                               ")
    print(" / _| / \  | | |  _ \ __ _ _ __ __ _ _ __ ___  ___ ")
    print("| |_ / _ \ | | | |_) / _` | '__/ _` | '_ ` _ \/ __|")
    print("|  _/ ___ \| | |  __/ (_| | | | (_| | | | | | \__ \\")
    print("|_|/_/   \_\_|_|_|   \__,_|_|  \__,_|_| |_| |_|\___/")
    print()
    print(colors.CYAN + "                            Developed by mha4065    " + colors.NOCOLOR)
    print(colors.YELLOW + "                                         mha4065.com" + colors.NOCOLOR)
    print()
    print()


user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6']

if args.help:
    parser.print_help()

# Get all keys from JSON content-type
def get_keys(data):
    params = []
    for key in data.keys():
        params.append(key)
        if isinstance(data[key], dict):
            for sub_key in data[key].keys():
                params.append(sub_key)
                if isinstance(data[key][sub_key], dict):
                    for sub_sub_key in data[key][sub_key].keys():
                        params.append(sub_sub_key)
                        if isinstance(data[key][sub_key][sub_sub_key], dict):
                            for sub_sub_sub_key in data[key][sub_key][sub_sub_key].keys():
                                params.append(sub_sub_sub_key)
        elif isinstance(data[key], list):
            for item in data[key]:
                if isinstance(item, dict):
                    for sub_key in item.keys():
                        params.append(sub_key)
                        if isinstance(item[sub_key], dict):
                            for sub_sub_key in item[sub_key].keys():
                                params.append(sub_sub_key)
                                if isinstance(item[sub_key][sub_sub_key], dict):
                                    for sub_sub_sub_key in item[sub_key][sub_sub_key].keys():
                                        params.append(sub_sub_sub_key)
    params = list(set(params))
    return params

# Crawling function
def crawling(url):
    try:
        if not args.no_logging:
            logger.info("Running crawler")

        # headless request
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        session = Session()
        if args.random_useragent:
            headers = {'User-Agent': choice(user_agents)}
            response = session.get(url, headers=headers)
        else:
            headers = {'User-Agent': 'User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}
            response = session.get(url, headers=headers)
        driver.quit()

        content_type = response.headers.get('content-type')

        if args.exclude:
            exclude = args.exclude.replace(' ', '').split(',')
        else:
            exclude = []
        # Check if content-type is JSON
        if 'application/json' in content_type and not 'json' in exclude:
            data = json_loads(response.content)
            params = get_keys(data)

        # Check if content-type is XML
        elif 'application/xml' in content_type and not 'xml' in exclude:
            params = []
            r = request_get(url)
            root = ET.fromstring(r.content)
            for child in root.iter('*'):
                child = str(child.tag)
                child = sub('{.+}', '', child)
                params.append(child)
            params = list(set(params))

        # Crawl HTML
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            tags = [tag.name for tag in soup.find_all()]
            params = []
            for tag in set(tags):
                elements = soup.find_all(tag)
                for element in elements:
                    if element.has_attr("id"):
                        params.append(element['id'])
                    if element.has_attr("name"):
                        params.append(element['name'])
                    if element.has_attr("href"):
                        if '?' in element['href']:
                            param = parse_qs(urlparse(element['href']).query)
                            param_names = [params.append(prm) for prm in param.keys()]
                        else:
                            pass

            # Javascript section
            scripts = soup.find_all("script")
            for script in scripts:
                matches = findall(r"(var|let|const)\s+(\w+)", script.text)
                for match in matches:
                    params.append(match[1])

                matches = findall(r"(\w+)\s*:", script.text)
                for match in matches:
                    params.append(match)

                matches = findall(r"(\w+)\s*=", script.text)
                for match in matches:
                    params.append(match)

            params = list(set(params))

        # Output
        if not args.silent:
            if args.output == '':
                for param in params:
                    print(param)
            else:
                for param in params:
                    with open(args.output, 'a') as f:
                        f.write(param+'\n')
        else:
            if args.output == '':
                for param in params:
                    print(param)
            else:
                for param in params:
                    with open(args.output, 'a') as f:
                        f.write(param+'\n')
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass
    else:
        if not args.no_logging:
            logger.info("Crawing is finished")
        pass
    
# Threading function
def thread(url):
    threads = []
    while len(threads) >= int(args.thread):
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
                break

    t = Thread(target=crawling, args=(url,))
    t.start()

    threads.append(t)

    for thread in threads:
        thread.join()

# Get a list of URLs
if args.list != '':
    urls = [line.strip() for line in open(args.list)]
    for url in urls:
        if not args.silent:
            print(colors.GREEN + '[+] ' + colors.NOCOLOR + url)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        thread(url)
# Get single URL
elif args.domain != '':
    url = args.domain
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    thread(url)
# Get input from pipeline stdin
else:
    if not stdin.isatty():
        input_urls = [line.strip() for line in stdin.readlines()]
        if len(input_urls) == 1:
            url = input_urls[0]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            
            thread(url)
        else:
            for url in input_urls:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "https://" + url
                thread(url)
    else:
        print()
        print(colors.RED + '[-] ' + colors.NOCOLOR + 'Provide an URL or a file')