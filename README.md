# fAllParams

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#tool-options">Tool options</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">license</a>
</p>

fAllParams is a powerful tool to extract all parameters from given URLs. It's also support `json` and `xml` content type. This tool has the ability to extract the parameters from the BurpSuite response (To use this feature, save the response of the desired URL in a file and then give it as input to the tool).

### Note
- This tool has the ability to send headless requests with Firefox or Chrome drivers

## Requirements
  - Python3
  - Firefox browser or Chrome browser

## Installation
  1. `git clone https://github.com/mha4065/fAllParams.git`
  2. `chmod +x fAllParams.py`
  
### Note
- You can also download the binary file of the tool from the releases and move it to `/usr/local/bin/` path
- `fAllParams -h`


### Tool Options
- `-d` or `--domain` : Provide an URL to get params. (To single URL check) - e.g. `-d/--domain domain.tld`
- `-l` or `--list` : Provide a file to get params. (To multiple URL check) - e.g. `-l/--list domains.txt`
- `-f` or `--file` : HTTP request response file - e.g. `-f/--file response.txt`
- `-s` or `--silent` : Run the tool in silent mode
- `-x` or `--exclude` : Exclude content-type - e.g. `-x/--exclude json,xml`
- `-o` or `--output` : Write output to a file
- `-t` or `--thread` : Specify threads - default: `1` - e.g. `-t/--thread 2`
- `-hl` or `--headless` : Headless driver (default: firefox driver) - e.g. `-hl/--headless chrome`
- `-nl` or `--no_logging` : Running the tool without saving logs, logs are saved by default
- `-ru` or `--random_useragent` : Random User-Agent


## Usage

Extract the parameters from single domain
```
./fAllParams.py -d domain.tld
```

Extract the parameters from a list of domains
```
./fAllParams.py -l domains.txt
```

Extract the parameters from the `BurpSuite` response file
```
./fAllParams.py -f response.txt
```

Specify threads
```
./fAllParams.py -d domain.tld -t 5
```

Run the tool in silent mode
```
./fAllParams.py -d domain.tld -s
```

Write output to a file
```
./fAllParams.py -d domain.tld -o output.txt
```

Run the tool without saving logs, logs are saved by default
```
./fAllParams.py -d domain.tld -nl
```

Run the tool with random User-Agent
```
./fAllParams.py -d domain.tld -ru
```

Exclude content-types:
```
./fAllParams.py -d domain.tld -x json,xml
```

Specify the headless driver:
```
./fAllParams.py -d domain.tld -hl chrome
```

You can also pipe your domain(s) to tools
```
echo domain.tld | fAllParams
```
```
cat domains.txt | fAllParams
```

## License
This project is licensed under the MIT license. See the LICENSE file for details.
