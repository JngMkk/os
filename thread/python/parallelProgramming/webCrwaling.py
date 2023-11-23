import concurrent.futures
import logging
import queue
import re
import sys
import threading

import requests  # noqa

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

link_regex = re.compile("<a\s(?:.*?\s)*?href=['\"](.*?)['\"].*?>")

urls = queue.Queue()
urls.put("https://www.google.com")
urls.put("https://br.bing.com")
urls.put("https://duckduckgo.com")
urls.put("https://github.com")
urls.put("https://br.search.yahoo.com")

result_dic = {}


def group_urls_task(urls: queue.Queue) -> None:
    try:
        # True: 동기화된 큐에 접근을 차단
        # timeout 0.05: 동기화된 큐에서 요소가 존재하지 않을 경우 너무 많이 기다리게 하는 것을 방지
        url = urls.get(True, 0.05)
        result_dic[url] = None
        logger.info(
            f"{threading.current_thread().name} putting url {url} in dictionary..."
        )
    except queue.Empty:
        logger.error("Nothing to be done, queue is empty.")


def crawl_task(url: str) -> tuple[str, list[str]]:
    links = []

    try:
        _request = requests.get(url)
        logger.info(f"{threading.current_thread().name} crawling url {url} ...")
        links = link_regex.findall(_request.text)
    except:
        logger.error(sys.exc_info()[0])
        raise
    finally:
        return (url, links)


# Threadpool: 이전에 생성했던 여러 스레드를 특정 프로세스에 사용하도록 유지함.
# 스레드 재사용에 목표를 두고 있기 때문에 비용이 많이 드는 불필요한 스레드 생성을 방지할 수 있음.
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as group_link_threads:
    for _ in range(urls.qsize()):
        # dispatch (멀티태스크 실행 시스템이 다음에 실행해야 하는 프로그램을 결정하여 CPU 사용권을 주는 조작)
        # submit 메서드는 실행을 위해 callable 객체를 스케줄링하고,
        # 실행을 위해 생성된 스케줄링을 포함한 Future 객체를 반환함.
        group_link_threads.submit(group_urls_task, urls)


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as crawl_link_threads:
    future_tasks = {
        crawl_link_threads.submit(crawl_task, url): url for url in result_dic.keys()
    }

    # 실행했던 예약으로부터 결과를 수집
    # as_complete 메서드를 이용해 future task에서 완료된 항목을 찾음.
    # 이 호출은 future 객체의 인스턴스에 대한 반복자를 반환.
    # 따라서 dispatch했던 예약으로 처리한 각 결과를 순환할 수 있음.
    for future in concurrent.futures.as_completed(future_tasks):
        result_dic[future.result()[0]] = future.result()[1]

for url, links in result_dic.items():
    logger.info(f"{url} with links: [{links[0]}, ...")


"""
각 풀에서의 스레드 실행 순서가 논리 순서를 나타내지 않는데, 니는 비결정성의 결과.

2023-11-23 16:23:00,845 - ThreadPoolExecutor-0_0 putting url https://www.google.com in dictionary...
2023-11-23 16:23:00,845 - ThreadPoolExecutor-0_0 putting url https://br.bing.com in dictionary...
2023-11-23 16:23:00,845 - ThreadPoolExecutor-0_0 putting url https://duckduckgo.com in dictionary...
2023-11-23 16:23:00,845 - ThreadPoolExecutor-0_0 putting url https://github.com in dictionary...
2023-11-23 16:23:00,845 - ThreadPoolExecutor-0_0 putting url https://br.search.yahoo.com in dictionary...
2023-11-23 16:23:00,851 - Starting new HTTPS connection (1): br.bing.com:443
2023-11-23 16:23:00,852 - Starting new HTTPS connection (1): duckduckgo.com:443
2023-11-23 16:23:00,857 - Starting new HTTPS connection (1): www.google.com:443
2023-11-23 16:23:00,891 - https://br.bing.com:443 "GET / HTTP/1.1" 302 0
2023-11-23 16:23:00,900 - Starting new HTTPS connection (1): www.bing.com:443
2023-11-23 16:23:01,077 - https://www.bing.com:443 "GET /?cc=br HTTP/1.1" 200 None
2023-11-23 16:23:01,092 - ThreadPoolExecutor-1_1 crawling url https://br.bing.com ...
2023-11-23 16:23:01,098 - https://www.google.com:443 "GET / HTTP/1.1" 200 None
2023-11-23 16:23:01,099 - ThreadPoolExecutor-1_0 crawling url https://www.google.com ...
2023-11-23 16:23:01,103 - Starting new HTTPS connection (1): br.search.yahoo.com:443
2023-11-23 16:23:01,103 - Starting new HTTPS connection (1): github.com:443
2023-11-23 16:23:01,136 - https://github.com:443 "GET / HTTP/1.1" 200 None
2023-11-23 16:23:01,146 - ThreadPoolExecutor-1_1 crawling url https://github.com ...
2023-11-23 16:23:01,183 - https://duckduckgo.com:443 "GET / HTTP/1.1" 200 2393
2023-11-23 16:23:01,183 - ThreadPoolExecutor-1_2 crawling url https://duckduckgo.com ...
2023-11-23 16:23:01,789 - https://br.search.yahoo.com:443 "GET / HTTP/1.1" 200 34103
2023-11-23 16:23:01,913 - ThreadPoolExecutor-1_0 crawling url https://br.search.yahoo.com ...
2023-11-23 16:23:01,916 - https://www.google.com with links: [https://www.google.com/imghp?hl=ko&tab=wi, ...
2023-11-23 16:23:01,916 - https://br.bing.com with links: [javascript:void(0);, ...
2023-11-23 16:23:01,916 - https://duckduckgo.com with links: [/about, ...
2023-11-23 16:23:01,916 - https://github.com with links: [#start-of-content, ...
2023-11-23 16:23:01,916 - https://br.search.yahoo.com with links: [/history, ...
"""
