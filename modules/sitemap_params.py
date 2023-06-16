from .html_function import html_crawling
from bs4 import BeautifulSoup
from re import findall, DOTALL, search, compile
from urllib.parse import urlparse, parse_qs
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

        # matches = findall(r"(\w+)\s*=", response)
        # for match in matches:
        #     js_params.append(match)

        matches = findall(r'[{,]\s*([A-Za-z0-9_]+)\s*:', response)
        if matches:
            for match in matches:
                js_params.append(match)

        scripts = findall(r"<script\b[^>]*>(.*?)</script>", response, DOTALL)
        for script in scripts:
            if not "text/template" in script:
                objects = findall(r'\{.*?\}', script)
                if len(objects) > 1:
                    obj_keys1 = findall(r'[,|{]\s*"([^"]*)"\s*:', str(objects))
                    for obj in obj_keys1:
                        js_params.append(obj)
                    obj_keys2 = findall(r'[,{]\\\\"?(.*?)"?\s*[:\\\\]', str(objects))
                    for obj in obj_keys2:
                        js_params.append(obj)
                    obj_keys3 = findall(r'[,{]\\\\"(.*?)\\\\":', str(objects))
                    for obj in obj_keys3:
                        js_params.append(obj)

        js_params = list(set(js_params))
        return js_params
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass

def post_get_requests_params(contents, logger, args):
    GET_params = []
    try:
        requests = findall(r'----- REQUEST(.*?)HTTP/', contents, DOTALL)
        for request in requests:
            parameters = findall(r'\b\w+=', request)
            for param in parameters:
                GET_params.append(param.rstrip('='))
        return GET_params
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass


def post_req_body(contents, exclude, logger, args):
    requests = findall("----- REQUEST\n(.*?)\n----- RESPONSE", contents, DOTALL)
    params = []
    for req in requests:
        try:
            if 'POST' in req:
                if "application/json" in req and not 'json' in exclude:
                    json_str = search("{.*}", req, DOTALL).group(0)
                    json_data = json.loads(json_str)
                    keys = list(json_data.keys())
                    for key in keys:
                        params.append(key)
                if "application/x-www-form-urlencoded" in req:
                    sections = req.split("\n\n")
                    if len(sections) > 1:
                        body = sections[1]
                        # Split the body into key-value pairs
                        pairs = body.split("&")
                        # Extract names with '='
                        for pair in pairs:
                            if "=" in pair:
                                name = pair.split("=")[0]
                                params.append(name)
                if "application/xml" in req and not 'xml' in exclude:
                    param_list = findall(r'<([^/].*?)>', req)
                    params.extend([param.strip() for param in param_list])
            else:
                pass
        except Exception as e:
            if not args.no_logging:
                logger.error(e)
            pass

    params = list(set(params))
    return params


def resp_body(contents, exclude, logger, args):
    requests = findall("----- RESPONSE\n(.*?)\n----- REQUEST", contents, DOTALL)
    params = []
    for req in requests:
        if "application/json" in req and not 'json' in exclude:
            try:
                sections = req.split("\n\n")
                if len(sections) > 1:
                    body = sections[1]
                    json_str = search("{.*}", body, DOTALL).group(0)
                    json_data = json.loads(json_str)
                    keys = list(json_data.keys())
                    for key in keys:
                        params.append(key)
            except Exception as e:
                if not args.no_logging:
                    logger.error(e)
                pass
        if "text/xml" in req and not 'xml' in exclude:
            try:
                param_list = findall(r'<([^/?].*?)>', req)
                params.extend([param.strip() for param in param_list])
            except Exception as e:
                if not args.no_logging:
                    logger.error(e)
                pass

    params = list(set(params))
    return params


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


def sitemap(args, logger):
    if args.exclude:
        exclude = args.exclude.replace(' ', '').split(',')
    else:
        exclude = []

    params = []
    with open(args.file, 'r', encoding='iso-8859-1') as f:
        contents = f.read()

        pattern = r'<html.*?>\s*(.*?)\s*</html>'

        matches = findall(pattern, contents, flags=DOTALL)
        for match in matches:

            soup = BeautifulSoup(match, "html.parser")

            # Exclude tags from response
            exclude_tags = ['meta', 'html', 'head']
            
            tags = []
            for tag in soup.find_all():
                if tag.name not in exclude_tags:
                    tags.append(tag.name)
                else:
                    pass
            
            for tag in set(tags):
                elements = soup.find_all(tag)
                try:
                    for element in elements:
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

        js_params = js_regex(contents, logger, args)
        GET_params = post_get_requests_params(contents, logger, args)
        post_rb = post_req_body(contents, exclude, logger, args)
        res_body = resp_body(contents, exclude, logger, args)
        js_obj = get_js_objects(contents, logger, args)

        merged_params = []
        merged_params.extend(js_params)
        merged_params.extend(GET_params)
        merged_params.extend(post_rb)
        merged_params.extend(res_body)
        merged_params.extend(js_obj)

        merged_params = list(set(merged_params))

        return merged_params