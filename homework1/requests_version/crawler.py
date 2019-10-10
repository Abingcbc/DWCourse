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
    for i in range(100):
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "user-agent": random.choice(user_agents),
        }
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        proxyUser = "H89052327LK4427D"
        proxyPass = "6E4DC2BFFB11A7B3"
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        proxies = {"http": proxyMeta, "https": proxyMeta}
        try:
            response = requests.get(
                url=url, headers=headers, proxies=proxies, timeout=20
            )
        except Exception as e:
            log(item['ID'] + ': ' + str(e))
            continue
        response_code = response.status_code
        response = BeautifulSoup(response.text, "lxml")
        if response_code != 200:
            if response_code == 404:
                with open("not_found.log", "a") as file:
                    file.write(item["ID"]+'\n')
                    return
            log("ErrorCode: " + str(response_code))
            continue
        elif not (response.find(name="title", text=re.compile("Robot Check")) is None):
            log("Robot check triggered")
            continue
        else:
            page_type = response.find(id="productTitle")
            if page_type is None:
                log("-" * 10 + item["ID"] + ": Prime" + "-" * 10)
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
                break
            else:
                log("-" * 10 + item["ID"] + ": Ordinary" + "-" * 10)
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
                break
    if recieved:
        write_result(item)
    else:
        with open("error.log", "a") as file:
            file.write(item["ID"] + "\n")
            file.write("Retry times overflow\n\n")


def run():
    item = {}
    url = start_urls.get()
    item["ID"] = url.split("/")[-1].strip()
    get_and_parse(url, item)

def crawl():
    threads = []

    for i in range(4):
        threads.append(threading.Thread(target=run))

    for i in range(len(threads)):
        threads[i].start()