##################################################
## File: crawler.py
## Auth: smoh
## Create: 20.01.21
## Desc: Redmine crawler using beautifulsoup.
##################################################

import requests
import datetime
from bs4 import BeautifulSoup

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
        return

    def main(self):
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
                print('Failed to login(Code: %d)' %(req.status_code))
            print(self.__issues)
        return

crawler = Crawler()
crawler.main()