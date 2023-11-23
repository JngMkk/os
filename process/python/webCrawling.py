import concurrent.futures
import logging
import queue
import re
import sys
from multiprocessing import Manager, cpu_count, current_process

import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def group_urls_task(urls: queue.Queue, result_dict: dict[str, str]) -> None:
    try:
        url = urls.get(True, 0.05)
        result_dict[url] = None
        logger.info(f"[{current_process().name}] putting url [{url}] in dictionary...")
    except queue.Empty:
        logger.error("Nothing to be done, queue is empty.")


def crawl_task(url: str, link_regex: re.Pattern) -> tuple[str, list[str]]:
    links = []

    try:
        _request = requests.get(url)
        logger.info(f"[{current_process().name}] crawling url {url} ...")
        links = link_regex.findall(_request.text)
    except:
        logger.error(sys.exc_info())
        raise
    finally:
        return (url, links)


if __name__ == "__main__":
    manager = Manager()
    number_of_cpus = cpu_count()

    urls = manager.Queue()
    urls.put("http://www.google.com")
    urls.put("http://br.bing.com/")
    urls.put("https://duckduckgo.com/")
    urls.put("https://github.com/")
    urls.put("http://br.search.yahoo.com/")

    link_regex = re.compile("<a\s(?:.*?\s)*?href=['\"](.*?)['\"].*?>")

    result_dict = manager.dict()
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=number_of_cpus
    ) as group_link_processes:
        for i in range(urls.qsize()):
            group_link_processes.submit(group_urls_task, urls, result_dict)

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=number_of_cpus
    ) as crawler_link_processes:
        future_tasks = {
            crawler_link_processes.submit(crawl_task, url, link_regex): url
            for url in result_dict.keys()
        }
        for future in concurrent.futures.as_completed(future_tasks):
            result_dict[future.result()[0]] = future.result()[1]

    for url, links in result_dict.items():
        logger.info(f"[{url}] with links : [{links[0]}, ...")


"""
2023-11-23 18:28:52,128 - [SpawnProcess-3] putting url [http://www.google.com] in dictionary...
2023-11-23 18:28:52,128 - [SpawnProcess-2] putting url [http://br.bing.com/] in dictionary...
2023-11-23 18:28:52,129 - [SpawnProcess-5] putting url [https://duckduckgo.com/] in dictionary...
2023-11-23 18:28:52,129 - [SpawnProcess-6] putting url [https://github.com/] in dictionary...
2023-11-23 18:28:52,131 - [SpawnProcess-4] putting url [http://br.search.yahoo.com/] in dictionary...
2023-11-23 18:28:52,227 - Starting new HTTP connection (1): br.search.yahoo.com:80
2023-11-23 18:28:52,227 - Starting new HTTP connection (1): www.google.com:80
2023-11-23 18:28:52,227 - Starting new HTTPS connection (1): duckduckgo.com:443
2023-11-23 18:28:52,227 - Starting new HTTP connection (1): br.bing.com:80
2023-11-23 18:28:52,234 - Starting new HTTPS connection (1): github.com:443
2023-11-23 18:28:52,242 - http://br.bing.com:80 "GET / HTTP/1.1" 302 0
2023-11-23 18:28:52,252 - Starting new HTTP connection (1): www.bing.com:80
2023-11-23 18:28:52,269 - https://github.com:443 "GET / HTTP/1.1" 200 None
2023-11-23 18:28:52,279 - [SpawnProcess-11] crawling url https://github.com/ ...
2023-11-23 18:28:52,296 - http://www.bing.com:80 "GET /?cc=br HTTP/1.1" 200 None
2023-11-23 18:28:52,308 - [SpawnProcess-7] crawling url http://br.bing.com/ ...
2023-11-23 18:28:52,377 - http://www.google.com:80 "GET / HTTP/1.1" 200 8306
2023-11-23 18:28:52,381 - [SpawnProcess-8] crawling url http://www.google.com ...
2023-11-23 18:28:52,455 - http://br.search.yahoo.com:80 "GET / HTTP/1.1" 301 25
2023-11-23 18:28:52,459 - Starting new HTTPS connection (1): br.search.yahoo.com:443
2023-11-23 18:28:52,534 - https://duckduckgo.com:443 "GET / HTTP/1.1" 200 2393
2023-11-23 18:28:52,534 - [SpawnProcess-9] crawling url https://duckduckgo.com/ ...
2023-11-23 18:28:53,070 - https://br.search.yahoo.com:443 "GET / HTTP/1.1" 200 34102
2023-11-23 18:28:53,189 - [SpawnProcess-10] crawling url http://br.search.yahoo.com/ ...
2023-11-23 18:28:53,206 - [http://www.google.com] with links : [https://www.google.com/imghp?hl=ko&tab=wi, ...
2023-11-23 18:28:53,206 - [http://br.bing.com/] with links : [javascript:void(0);, ...
2023-11-23 18:28:53,206 - [https://duckduckgo.com/] with links : [/about, ...
2023-11-23 18:28:53,206 - [https://github.com/] with links : [#start-of-content, ...
2023-11-23 18:28:53,206 - [http://br.search.yahoo.com/] with links : [/history, ...
"""
