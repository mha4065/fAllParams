# fAllParams

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#tool-options">Tool options</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">license</a>
</p>

fAllParams is a powerful tool to extract all parameters from given URLs. It's also support `json` and `xml` content type.

### Note
- This tool uses Firefox to send headless requests

## Requirements
  - Python3
  - Firefox browser

## Installation
  1. `git clone https://github.com/mha4065/fAllParams.git`
  2. `chmod +x fAllParams.py`
  
### Note
- You can also download the binary file of the tool from the releases and move it to `/usr/local/bin` path
- `fAllParams -h`


### Tool Options
- `-d` or `--domain` : Provide an URL to get params. (To single URL check) - e.g. `-d/--domain domain.tld`
- `-l` or `--list` : Provide a file to get params. (To multiple URL check) - e.g. `-l/--list domains.txt`
- `-t` or `--thread` : Specify threads - default: `1` - e.g. `-t/--thread 2`
- `-s` or `--silent` : Run the script silently and do not display any output
- `-o` or `--output` : Write output to a file
- `-ru` or `--random_useragent` : Random User-Agent
- `-x` or `--exclude` : Exclude content-type - e.g. `-x/--exclude json,xml`
- `-nl` or `--no_logging` : Running the tool without saving logs, logs are saved by default

## Usage

Find the parameters of a domain
```
./fAllParams.py -d domain.tld
```

Find the parameters of a list of domains
```
./fAllParams.py -l domains.txt
```

Specify threads
```
./fAllParams.py -d domain.tld -t 5
```

Silent mode
```
./fAllParams.py -d domain.tld -s
```

Write output to a file
```
./fAllParams.py -d domain.tld -o output.txt
```

Running the tool without saving logs, logs are saved by default
```
./fAllParams.py -d domain.tld -nl
```

Running the tool with random User-Agent
```
./fAllParams.py -d domain.tld -ru
```

Exclude content-types:
```
./fAllParams.py -d domain.tld -x json,xml
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
