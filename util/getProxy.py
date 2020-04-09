import requests

def get_proxy_ip(url):
    proxy = requests.get(url).text.strip('\n')
    return proxy