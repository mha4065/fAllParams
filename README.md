# fAllParams

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#tool-options">Tool options</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">license</a>
</p>

fAllParams is a powerful tool for extracting all parameters from given URLs.

### Note
- This tool has the ability to send headless requests with Firefox or Chrome drivers
- This tool also supports `json` and `xml` content types. 
- This tool has the ability to extract parameters from the `BurpSuite` site map (to use this feature, extract the site map generated for the desired domain in a `txt` file using the `Burp Suite Site Map Extractor` extension, and then as input to the tool by give `-f`)

## Requirements
- Python3
- Firefox or Chrome browser or Chromium driver only

## Installation
  1. `git clone https://github.com/mha4065/fAllParams.git`
  2. `pip3 install -r requirements.txt`
  3. `chmod +x fAllParams.py`
  4. `./fAllParams.py -h`
  
### Note
- You can also download the binary file of the tool from the releases and move it to `/usr/local/bin/` path
- `fAllParams -h`


### Tool Options
- `-u` or `--url` : Single URL
- `-l` or `--list` : URL list file. (To multiple URL check)
- `-f` or `--file` : Enter your BurpSuite site map txt file
- `-s` or `--silent` : Run the tool in silent mode
- `-x` or `--exclude` : Exclude content-type, for example `json` or `xml`
- `-H` or `--header` : Enter your custom headers
- `-o` or `--output` : Write output to a file
- `-t` or `--thread` : Specify threads - default: `2`
- `-hl` or `--headless` : Send request in headless mode
- `-dp` or `--driver_path` : Full path to the browser driver to use
- `-nl` or `--no_logging` : Running the tool without saving logs, logs are saved by default
- `-ua` or `--user_agent` : Enter your user-agent. By default, the user-agent is randomly selected
- `-px` or `--proxy`: Enter your proxy
- `-js` or `--javascript` : Sending request and crawling the response of the entire site's JavaScript files
- `-aa` or `--all_attributes` : Extracting all attributes of HTML tags. (not recommended)
- `-h` or `--help` : Display help message


## Usage

Extract the parameters from single URL
```
./fAllParams.py -u domain.tld/path1/path2/path3
```

Extract the parameters from a list of URL
```
./fAllParams.py -l urls.txt
```

Extract the parameters from the `BurpSuite` site map (to use this feature, extract the site map generated for the desired domain in a `txt` file using the `Burp Suite Site Map Extractor` extension, and then as input to the tool by give `-f`)
```
./fAllParams.py -f sitemap.txt
```

### Note
- You can download this extension from the following URL:
- `https://github.com/PortSwigger/site-map-extractor`

Specify threads
```
./fAllParams.py -u domain.tld/path1/path2/path3 -t 5
```

Run the tool in silent mode
```
./fAllParams.py -u domain.tld/path1/path2/path3 -s
```

Write output to a file
```
./fAllParams.py -u domain.tld/path1/path2/path3 -o output.txt
```

Run the tool without saving logs, logs are saved by default
```
./fAllParams.py -u domain.tld/path1/path2/path3 -nl
```

Run the tool with your User-Agent
```
./fAllParams.py -u domain.tld/path1/path2/path3 -ua "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"
```

Exclude content-types:
```
./fAllParams.py -u domain.tld/path1/path2/path3 -x json,xml
```

Specify headers:
```
./fAllParams.py -u domain.tld/path1/path2/path3 -H "Cookie: yourcookie" -H "X-Forwarded-For: 127.0.0.1"
```

Send request in headless mode:
```
./fAllParams.py -u domain.tld/path1/path2/path3 -hl chrome -dp /path/to/chromedriver
```

Sending request and crawling the response of the entire site's JavaScript files:
```
./fAllParams.py -u domain.tld/path1/path2/path3 -js
```

HTTP proxy to use
```
./fAllParams.py -u domain.tld/path1/path2/path3 -px "http://ip:port"
```

Extracting all attributes of HTML tags. (not recommended):
```
./fAllParams.py -u domain.tld/path1/path2/path3 -aa
```

You can also pipe your URL(s) to tools
```
echo domain.tld/path1/path2/path3 | fAllParams
```
```
cat urls.txt | fAllParams
```

## License
This project is licensed under the MIT license. See the LICENSE file for details.
