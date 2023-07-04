from selenium.webdriver.firefox.options import Options as firefox_option
from selenium.webdriver.chrome.options import Options as chrome_option
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.firefox.service import Service as firefox_service
from seleniumwire import webdriver
from random import choice
from tldextract import extract as tld_extract
from modules.agents import user_agents

def headless_function(args, url):

    wire_options = {}
    
    if args.proxy:
        wire_options = {
            'proxy': {
                'http': args.proxy,
                'https': args.proxy,
                'no_proxy': None
        }
}

    if args.headless == "firefox":
        if args.driver_path:
            service = firefox_service(executable_path=args.driver_path)
            options = firefox_option()
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            driver = webdriver.Firefox(options=options, seleniumwire_options=wire_options, service=service)
        else:
            options = firefox_option()
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            driver = webdriver.Firefox(options=options, seleniumwire_options=wire_options)
    else: 
        if args.driver_path:
            service = chrome_service(executable_path=args.driver_path)
            options = chrome_option()
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options, seleniumwire_options=wire_options, service=service)
        else:
            options = chrome_option()
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options, seleniumwire_options=wire_options)
    
    def interceptor(request):
        del request.headers['User-Agent']
        del request.headers['user-agent']
        if args.user_agent:
            request.headers['user-agent'] = args.user_agent
        else:
            request.headers['user-agent'] = choice(user_agents)
        
        if args.header:
            for option in args.header:
                key, value = option.split(':')
                request.headers[key] = value

    driver.request_interceptor = interceptor
    driver.get(url)
    
    get_domain = tld_extract(url).domain
    content_type = ""
    for request in driver.requests:
        if get_domain in request.host:
            content_type = driver.requests[0].response.headers['Content-Type']
            break

    response = driver.page_source
    driver.close()
    return response, content_type