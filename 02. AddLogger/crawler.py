##################################################
## File: crawler.py
## Auth: smoh
## Create: 20.02.03
## Desc: Redmine crawler using beautifulsoup.
## Updated
##      20.02.03. smoh - Add signal hadler and logger. 
##################################################

import requests
import datetime
import time
import signal
import os
from bs4 import BeautifulSoup
from logger import Logger

class Crawler:
    def __init__(self):
        self.__main_url = 'https://src.smoh.kr/'
        self.__login_url = 'https://src.smoh.kr/login'
        self.__search_url = 'https://src.smoh.kr/projects/crawlerissues/issues?set_filter=1'
        self.__login_data = {
            'username': 'jd_user',
            'password': 'P@ssword'
        }
        self.__issues = {}
        self.__stop = False;
        self.__log_file = 'D:\\crawler.log'

        self.logger = Logger('crawler', self.__log_file)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        return

    def stop(self, signum, frame):
        self.__stop = True
        return

    def main(self):
        self.logger.log('start', { 'pid': os.getpid() })
        while not self.__stop:
            with requests.Session() as s:
                main_req = s.get(self.__main_url)
                html = main_req.text
                obj = BeautifulSoup(html, 'html.parser')
                auth_token = obj.find('input', {'name': 'authenticity_token'})['value']
                self.__login_data = {**self.__login_data, **{'authenticity_token': auth_token}}

                login_req = s.post(self.__login_url, self.__login_data)
                if login_req.status_code == 200:
                    search_req = s.get(self.__search_url)
                    search_obj = BeautifulSoup(search_req.text, 'html.parser')
                    thead = search_obj.select('div.autoscroll > table > thead > tr > th')
                    tbody = search_obj.select('div.autoscroll > table > tbody > tr > td')
                    issue_obj = {}
                    issue_list = []
                    for i in range(1, len(tbody) +1):
                        if(i % len(thead) != 0):
                            issue_obj[thead[i % len(thead)].text] = tbody[i].text
                        else:
                            issue_list.append(issue_obj)
                            issue_obj = {}
                    self.__issues = {
                        'execution_dttm': str(datetime.datetime.now().isoformat()),
                        'issues': issue_list
                    }
                else:
                    self.logger.log('login_fail', { 
                        'pid': os.getpid(), 
                        'error_code':  req.status_code
                    })
                self.logger.log('get_issues', { 
                    'pid': os.getpid(),
                    'count': len(issue_list)
                })
                print(self.__issues)
                time.sleep(5)
        self.logger.log('stop', { 'pid': os.getpid() })
        return

crawler = Crawler()
crawler.main()