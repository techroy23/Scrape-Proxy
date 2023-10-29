import requests
from tabulate import tabulate
import random
import os

# URLs to collect proxies from
proxy_urls = [
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt"
]

# Websites to test proxies with
test_websites = [
    "https://icanhazip.com",
    "https://api.ipify.org"
]

# Collect all proxies
proxy_list = []
for url in proxy_urls:
    response = requests.get(url)
    proxies = response.text.split("\n")
    proxy_list.extend(proxies)

# Remove duplicates
proxy_list = list(set(proxy_list))
print("Total proxies: ", len(proxy_list))

# Function to test a proxy
def test_proxy(proxy):
    results = []
    for website in test_websites:
        try:
            print("Checking proxy", proxy, "with website", website)
            response = requests.get(website, proxies={"http": "socks5://" + proxy, "https": "socks5://" + proxy}, timeout=15)
            latency = response.elapsed.total_seconds()
            results.append([proxy.split(':')[0], proxy.split(':')[1], website, response.status_code, response.text.strip(), latency])
        except Exception as e:
            # print(f"Proxy {proxy} failed on {website} with error {str(e)}")
            print("Proxy", proxy, "is not working\n")
            return None
    return results

# Check if PROXY_SOCKS5.txt exists and test it
if os.path.exists("PROXY_SOCKS5.txt"):
    with open("PROXY_SOCKS5.txt", "r") as file:
        proxy = file.read().strip()
        print(f"Testing saved proxy: {proxy}")
        results = test_proxy(proxy)
        if results is not None:
            print("\n")
            print(tabulate(results, headers=["PROXY", "PORT", "WEBSITE", "RESPONSE CODE", "WEBSITE REPLY", "LATENCY IN SEC"], tablefmt="pretty"))
            exit(0)

# If PROXY_SOCKS5.txt does not exist or the saved proxy failed, pick a random proxy from the list and test it
while len(proxy_list) > 0:
    proxy = random.choice(proxy_list)
    print(f"Testing random proxy: {proxy}")
    results = test_proxy(proxy)
    if results is not None:
        print("\n")
        print(tabulate(results, headers=["PROXY", "PORT", "WEBSITE", "RESPONSE CODE", "WEBSITE REPLY", "LATENCY IN SEC"], tablefmt="pretty"))
        with open("PROXY_SOCKS5.txt", "w") as file:
            file.write(proxy)
        break
    else:
        proxy_list.remove(proxy)
