"""
Crawl 4 coreinfrastructure
"""
import csv
import requests
from bs4 import BeautifulSoup

__author__ = "vcancy"


# /usr/bin/python
# -*-coding:utf-8-*-

class Crawl:
    """ Crawl constructor """
    def __init__(self):
        self._request = requests.session()
        self._url = 'https://www.coreinfrastructure.org/programs/census-project'
        self._result = []
        self._out_file = 'out.csv'
        self._max_page = None
        self._first_load = True
        self._stop = False
        self._cur = 1

    def _out(self):
        """ Export crawl data to a csv file """
        titles = [
            'Title',
            'Risk Index',
            'CVE Count',
            'Contributor Count',
            'Popularity'
        ]
        with open(self._out_file, 'w') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quoting=csv.QUOTE_MINIMAL)
            spam_writer.writerow(titles)
            for entry in self._result:
                spam_writer.writerow(entry)

    def run(self):
        """ Process """
        while not self._stop:
            self._parse()
        self._out()
        self._request.close()

    def _parse(self):
        """ Request url and parse data to store """
        url = self._url if self._first_load else '{}?page={}'.format(self._url, self._cur)
        print('start crawl {}'.format(url))
        response = self._request.get(url)
        bs_obj = BeautifulSoup(response.text, 'lxml')
        rows = bs_obj.select('tbody')[0].select('tr')
        if self._first_load:
            self._max_page = int(bs_obj.
                                 find('a', {'title': 'Go to last page'})
                                 .get('href').split('=')[1])
            self._first_load = False
        else:
            self._cur += 1
            if self._cur > self._max_page:
                self._stop = True
        for row in rows:
            row_list = [str(_.text).replace('\n', '').replace(' ', '') for _ in row.select('td')]
            self._result.append(row_list)
        print('page count:{}'.format(len(rows)))


if __name__ == '__main__':
    crawl = Crawl()
    crawl.run()