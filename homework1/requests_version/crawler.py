import requests
from threading import Thread
from utils import *
import random
from init import start_urls, user_agents
from bs4 import BeautifulSoup
import re
import prime_parser
import ordinary_parser
import threading


def get_and_parse(url, item):
    recieved = False
    appKey = "Um1lYWlLRTBMbkVLWlN5NTphUzZHY0VGanVOc1RjSzJv"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "user-agent": random.choice(user_agents),
        "Proxy-Authorization": 'Basic '+ appKey
    }
    ip_port = 'secondtransfer.moguproxy.com:9001'
    proxies = {"http": "http://" + ip_port,"https": "https://" + ip_port}
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=20, verify=False, allow_redirects=False)
    except Exception as e:
        log(item["ID"] + ": " + str(e))
        start_urls.put(url)
        return
    response_code = response.status_code
    if response_code != 200:
        if response_code == 404:
            with open("not_found.log", "a") as file:
                file.write(item["ID"] + "\n")
                return
        log("ErrorCode: " + str(response_code))
        start_urls.put(url)
        return
    else:
        response = BeautifulSoup(response.text, "lxml")
        if not (response.find(name="title", text=re.compile("Robot Check")) is None):
            log("Robot check triggered")
            start_urls.put(url)
            return
        else:
            page_type = response.find(id="productTitle")
            if page_type is None:
                # log("-" * 10 + item["ID"] + ": Prime" + "-" * 10)
                item["name"], item["star_score"], item["imdb_score"], item[
                    "time_len"
                ], item["year"], item["restrict_level"], item["rent_price"], item[
                    "buy_price"
                ], item[
                    "meta_info"
                ], item[
                    "validation"
                ] = prime_parser.prime_parse(
                    response, item["ID"]
                )
                recieved = True
            else:
                # log("-" * 10 + item["ID"] + ": Ordinary" + "-" * 10)
                item["name"], item["star_score"], item["imdb_score"], item[
                    "time_len"
                ], item["year"], item["restrict_level"], item["rent_price"], item[
                    "buy_price"
                ], item[
                    "meta_info"
                ], item[
                    "validation"
                ] = ordinary_parser.ordinary_parse(
                    response, item["ID"]
                )
                recieved = True
    if recieved:
        write_result(item)

def run():
    item = {}
    url = start_urls.get()
    item["ID"] = url.split("/")[-1].strip()
    get_and_parse(url, item)


def crawl():
    threads = []

    for i in range(5):
        threads.append(threading.Thread(target=run))

    for i in range(len(threads)):
        threads[i].start()
