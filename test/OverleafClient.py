import cloudscraper
import browser_cookie3
from http import cookiejar
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
from pprint import pprint
import time
from datetime import datetime
from requests import cookies
import socketio
import threading
import requests
import html
import time
import random
import asyncio


from constants import Route, Locations
from utility import cookies_to_header
from OverleafWS import OverleafWS

class OverleafClient:
    def __init__(self,debug=False) -> None:

        self.cookies = browser_cookie3.firefox(domain_name=Route.HOST)
        self.scraper = cloudscraper.create_scraper(    
                                                   browser={
                                                       'browser': 'firefox',
                                                       'platform': 'linux',
                                                       'mobile': False

                                                       }

                                                   )
        if debug:
            os.environ['REQUESTS_CA_BUNDLE'] = '/home/julienr/Downloads/burp_bundle.pem'
            self.scraper.proxies = {
                    "http": "http://127.0.0.1:8080",
                    "https": "http://127.0.0.1:8080"
                    }
            self.scraper.verify= "/home/julienr/Downloads/burp_bundle.pem"
        self.headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1",

                }
        self.scraper.cookies.update(self.cookies)

    def __get(self,url:str,stream=False):
        response = self.scraper.get(url,headers=self.headers,stream=stream)
        print(f"{url} fetched!")
        print(f"Status code: {response.status_code}")
        return response

    def fetch_all_projects(self):
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        response = self.__get(Route.MAIN + Route.PROJECT)
        with open(f"{Locations.RESPONSE}overleaf_fetch_project_{ts}.html","w+") as file:
            file.write(response.text)
        return response

    def parse_project_names(self,response):
        soup = BeautifulSoup(response.text, "html.parser")

        meta = soup.find("meta", {"name": "ol-prefetchedProjectsBlob"})
        if meta is None:
            raise Exception("No content")

        data = json.loads(html.unescape(str(meta["content"])))

        return data

    def choose_project(self):
        self.data = self.parse_project_names(self.fetch_all_projects())
        counter = 1
        ids = []
        for p in self.data["projects"]:
            print(f"[{counter}]{p["name"]}")
            ids.append(p["id"])
            counter+=1
        return ids[int(input("Choose a project id: "))-1]

    def fetch_project(self,id):
        # Step 1: HTTP handshake to get token
        t = int(time.time() * 1000) + random.randint(0, 1000)
        url= Route.MAIN + Route.SOCKETIO +f"?projectId={id}&t={t}"
        response = self.__get(url)
        
        # Response format: "token:heartbeat_timeout:connection_timeout:transports"
        parts = response.text.split(":")
        token = parts[0]
        print(f"Got token: {token}")

        # Step 2: Connect WebSocket
        ows = OverleafWS(self.scraper.cookies, Route.HOST)
        asyncio.run(ows.connect(token, id))

    
    def fetch_doc(self,id):
        resp = self.__get(Route.MAIN + Route.PROJECT+ Route.DOWNLOAD, stream=True)
        resp.raise_for_status()
        with open("file.zip", "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        








