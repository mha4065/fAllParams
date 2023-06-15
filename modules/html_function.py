from re import findall,DOTALL,search
from urllib.parse import urlparse, parse_qs
from tldextract import extract as tld_extract
from bs4 import BeautifulSoup
from requests import get as requests_get
import json


def js_regex(response, logger, args):
    js_params = []
    try:
        matches = findall(r"(var|let|const)\s+(.+?)(?:\s*=\s*.+)?\s*;", response)
        for match in matches:
            var_type, var_names = match[0], match[1]
            var_names_list = [name.strip() for name in var_names.split(',')]
            for var in var_names_list:
                js_params.append(var)

        matches = findall(r"(\w+)\s*:", response)
        for match in matches:
            js_params.append(match)

        matches = findall(r"(\w+)\s*=", response)
        for match in matches:
            js_params.append(match)

        matches = findall(r'[{,]\s*([A-Za-z0-9_]+)\s*:', response)
        if matches:
            for match in matches:
                js_params.append(match)

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


def get_js_objects(contents, logger, args):
    params = []

    def print_json_keys(obj_dict):
        for key in obj_dict.keys():
            clean_key = key.replace('@', '')
            params.append(clean_key)
            if isinstance(obj_dict[key], dict):
                print_json_keys(obj_dict[key])
            elif isinstance(obj_dict[key], list):
                for item in obj_dict[key]:
                    if isinstance(item, dict):
                        print_json_keys(item)

    soup = BeautifulSoup(contents, 'html.parser')
    try:
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        js_object = json.loads(script_tag.string)
        print_json_keys(js_object)
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass


    try:
        script_tag = soup.find('script', {'type': 'application/json'})
        json_object = json.loads(script_tag.string)
        print_json_keys(json_object)
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass

    def print_keys(obj_dict):
        for key in obj_dict.keys():
            params.append(key.replace('@', ''))
            if isinstance(obj_dict[key], dict):
                print_keys(obj_dict[key])
    

    scripts = soup.find_all('script')
    
    for script in scripts:
        if 'var' in script.text:
            match = search(r'var\s+(\w+)\s+=\s+(\{.+\});', script.text)
            if match:
                obj_data = match.group(2)
                try:
                    obj_dict = json.loads(obj_data)
                    print_keys(obj_dict)
                except Exception as e:
                    if not args.no_logging:
                        logger.error(e)
                    pass

    params = list(set(params))
    return params

def html_crawling(contents, url, logger, args):
    soup = BeautifulSoup(contents, "html.parser")
    
    tags = [tag.name for tag in soup.find_all()]
    params = []
    for tag in set(tags):
        elements = soup.find_all(tag)
        for element in elements:
            try:
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
    js_src_params = script_src(soup, logger, args, url)
    js_obj = get_js_objects(contents, logger, args)
            
    merged_params = []
    merged_params.extend(params)
    merged_params.extend(js_params)
    merged_params.extend(js_src_params)
    merged_params.extend(js_obj)

    merged_params = list(set(merged_params))
    return merged_params