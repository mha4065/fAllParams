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
  
### Note
- You can also download the binary file of the tool from the releases and move it to `/usr/local/bin/` path
- `fAllParams -h`


### Tool Options
- `-u` or `--url` : Single URL - e.g. `-u/--url domain.tld/path1/path2/path3`
- `-l` or `--list` : URL list file. (To multiple URL check) - e.g. `-l/--list urls.txt`
- `-f` or `--file` : BurpSuite site map txt file - e.g. `-f/--file sitemap.txt`
- `-s` or `--silent` : Run the tool in silent mode
- `-x` or `--exclude` : Exclude content-type - e.g. `-x/--exclude json,xml`
- `-o` or `--output` : Write output to a file
- `-t` or `--thread` : Specify threads - default: `2` - e.g. `-t/--thread 2`
- `-hl` or `--headless` : Send request in headless mode - e.g. `-hl/--headless chrome`
- `-dp` or `--driver_path` : Full path to the browser driver to use - `e.g. -hl/--headless chrome -dp/--driver_path /path/to/chromedriver`
- `-nl` or `--no_logging` : Running the tool without saving logs, logs are saved by default
- `-ru` or `--random_useragent` : Random User-Agent
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

Run the tool with random User-Agent
```
./fAllParams.py -u domain.tld/path1/path2/path3 -ru
```

Exclude content-types:
```
./fAllParams.py -u domain.tld/path1/path2/path3 -x json,xml
```

Send request in headless mode:
```
./fAllParams.py -u domain.tld/path1/path2/path3 -hl chrome -dp /path/to/chromedriver
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
