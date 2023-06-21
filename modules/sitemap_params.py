from .html_function import html_crawling
from bs4 import BeautifulSoup
from re import findall, DOTALL
from urllib.parse import urlparse, parse_qs
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

def post_get_req_params(contents, logger, args):
    params = []
    try:
        requests = findall(r'[GET|POST](.*?)HTTP\/', contents, DOTALL)
        for request in requests:
            parameters = findall(r'\b\w+=', request)
            for param in parameters:
                params.append(param.rstrip('='))
    except Exception as e:
        if not args.no_logging:
            logger.error(e)
        pass

    params = list(set(params))
    return params

def post_req_params(contents, exclude, logger, args):
    requests = findall("----- REQUEST\n(.*?)\n----- RESPONSE", contents, DOTALL)
    params = []
    for req in requests:
        try:
            if 'POST' in req:
                if "application/x-www-form-urlencoded" in req:
                    sections = req.split("\n\n")
                    if len(sections) > 1:
                        body = sections[1]
                        pairs = body.split("&")
                        for pair in pairs:
                            if "=" in pair:
                                name = pair.split("=")[0]
                                params.append(name)
            else:
                pass
        except Exception as e:
            if not args.no_logging:
                logger.error(e)
            pass

    params = list(set(params))
    return params

def xml_resp_req_body(contents, exclude, logger, args):
    response_body = findall("<\?xml.*?\?>[\s\S]*?(?=----- REQUEST)", contents, DOTALL)
    params = []
    illegal = ['!--', 'svg', '!DOCTYPE']
    for res in response_body:
        if not 'xml' in exclude:
            try:
                param_list = findall(r'<([^/?].*?)[\s|>]', res)
                for param in param_list:
                    if not param.rstrip() in illegal:
                        params.append(param.strip())
            except Exception as e:
                if not args.no_logging:
                    logger.error(e)
                pass

    request_body = findall("----- REQUEST\n(.*?)\n----- RESPONSE", contents, DOTALL)
    for req in request_body:
        if '<?xml' in req and not 'xml' in exclude:
            try:
                param_list = findall(r'<([^/?].*?)[\s|>]', req)
                for param in param_list:
                    if not param.rstrip() in illegal:
                        params.append(param.strip())
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
        pg_params = post_get_req_params(contents, logger, args)
        post_params = post_req_params(contents, exclude, logger, args)
        xml = xml_resp_req_body(contents, exclude, logger, args)

        merged_params = []
        merged_params.extend(js_params)
        merged_params.extend(pg_params)
        merged_params.extend(post_params)
        merged_params.extend(xml)

        merged_params = list(set(merged_params))

        return merged_params