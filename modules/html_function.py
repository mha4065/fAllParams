from re import findall,DOTALL,search
from urllib.parse import urlparse, parse_qs
from tldextract import extract as tld_extract
from bs4 import BeautifulSoup
from requests import get as requests_get
import json


def get_keys_from_json(json_data, keys):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            keys.append(key)
            if isinstance(value, (dict, list)):
                get_keys_from_json(value, keys)
    elif isinstance(json_data, list):
        for item in json_data:
            get_keys_from_json(item, keys)

def get_keys_from_text(text):
    pattern = r'(\s|\,)(\{.*?\})(\s|$)'
    matches = findall(pattern, text)
    keys = []
    for match in matches:
        try:
            obj = json.loads(match[1])
            get_keys_from_json(obj, keys)
        except ValueError:
            pass
    return keys

def js_regex(response, logger, args):
    js_params = []
    try:
        matches = findall(r"(var|let|const)\s+(\w+)", response)
        for match in matches:
            js_params.append(match[1])

        keys = get_keys_from_text(response)
        for key in keys:
            js_params.append(key)

        js_params = list(set(js_params))
        return js_params
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass


def script_src(soup, logger, args, url):
    js_src_params = []
    res = tld_extract(url).domain
    for script in soup.select('script[src]'):
        try:
            src = script['src']
            if script['src'].startswith("/"):
                if url.endswith('/'):
                    js_url = url + script['src'].replace('/', '')
                else:
                    js_url = url + script['src']
                resp = requests_get(js_url)
                js_src = js_regex(resp.text, logger, args)
                for jsparam in js_src:
                    js_src_params.append(jsparam)
            elif script['src'].startswith("//"):
                if url.endswith('/'):
                    js_url = url + script['src'].replace('//', '')
                else:
                    js_url = url + script['src'].replace('//', '/')
                resp = requests_get(js_url)
                js_src = js_regex(resp.text, logger, args)
                for jsparam in js_src:
                    js_src_params.append(jsparam)
            elif res in script['src']:
                resp = requests_get(script['src'])
                js_src = js_regex(resp.text, logger, args)
                for jsparam in js_src:
                    js_src_params.append(jsparam)
            else:
                pass
        except Exception as e:
            if not args.no_logging:
                logger.error(e)
            pass

    return js_src_params

def html_crawling(contents, url, logger, args):
    soup = BeautifulSoup(contents, "html.parser")
    # Exclude tags from response
    exclude_tags = ['meta', 'html', 'head']
    
    tags = []
    for tag in soup.find_all():
        if tag.name not in exclude_tags:
            tags.append(tag.name)
        else:
            pass

    params = []
    for tag in set(tags):
        elements = soup.find_all(tag)
        for element in elements:
            try:
                if args.all_attributes:
                    for value in element.attrs.values():
                        if value:
                            if isinstance(value, list):
                                for val in value:
                                    params.append(val)
                            else:
                                params.append(value)
                else:
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
            except Exception as e:
                if not args.no_logging:
                    logger.error(e)
                pass


    # Javascript section
    js_src_params = []
    js_params = js_regex(contents, logger, args)
    if args.javascript:
        js_src_params = script_src(soup, logger, args, url)
            
    merged_params = []
    merged_params.extend(params)
    merged_params.extend(js_params)
    if args.javascript:
        merged_params.extend(js_src_params)
        
    merged_params = list(set(merged_params))
    return merged_params