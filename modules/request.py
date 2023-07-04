from random import choice
from requests import get
from modules.agents import user_agents

def request_function(args, url):
    config_options = {}
    if args.header:
        for option in args.header:
            key, value = option.split(':')
            if args.user_agent:
                config_options['User-Agent'] = args.user_agent
            else:
                config_options['User-Agent'] = choice(user_agents)
            config_options[key] = value
    
    proxy = {}
    if args.proxy:
        proxy = {
            'http': args.proxy,
            'https': args.proxy
        }

    response = get(url, headers=config_options, proxies=proxy, verify=False)

    return response