
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen
from ast import literal_eval
import argparse, time, write_xlsx


class Zacks_Scraper(object):

    def __init__(self, input_path, write_path, text_file):
        self.stock_dates = {}   # {'aapl': [("7/25/2017", "After Close"), ()]}
        self.input_path = input_path
        self.write_path = write_path
        self.stocks = self.prep_tickers(self.input_path)
        self.text_file = text_file
        self.count = 0

    def get_stocks_for_date(self, url, name, count, part):
        print(
            '******** getting earnings dates for stock_name: %s, stock_count: %d, part: %s' %
            (name, count, part))
        check = True
        try:
            response = urlopen(url)
            html = response.read()
        except URLError as e:
            print(e.code)
            check = False
            time.sleep(1)
        if check:
            soup = BeautifulSoup(html, 'lxml')
            for s in soup.find_all('script'):
                for c in s.contents:
                    if 'document.obj_data' in c:
                        d = c.split('\n')
                        for index, x in enumerate(d):
                            if "earnings_announcements_earnings_table" in x:
                                y = index + 1
                                for x in d[y].split('] ,'):
                                    t = x.replace(
                                        '[', '').replace(
                                        ']', '').split(',')
                                    if name in self.stock_dates:
                                        self.stock_dates[name].append(
                                            (str(t[0].replace(' ', '')), str(t[-1].replace(' ', ''))))
                                    else:
                                        self.stock_dates[name] = [
                                            (str(t[0].replace(' ', '')), str(t[-1].replace(' ', '')))]
                                break
        else:
            print('stock threw error for url')

    def prep_tickers(self, path):
        with open(path, 'r') as myfile:
            data = myfile.read().replace('\n', '')

        stocks = literal_eval(data)
        return stocks

    def run_the_stocks(self, stocks, part):
        for name in stocks:
            self.count += 1
            url = 'https://www.zacks.com/stock/research/%s/earnings-announcements' % (name)
            self.get_stocks_for_date(url, name, self.count, part)
            time.sleep(.1)

    def write_data_txt_excel(self, part):
        if part == 3:
            if  self.text_file:
                write_path = '%sstocks_dates_%s.txt' % (self.write_path, 'universe')
                open(write_path, 'w').close()
                with open(write_path, 'r+') as g:
                    g.write(str(self.stock_dates))
            else:
                write_path = '%sstocks_dates_%s.xlsx' % (self.write_path, 'universe')
                write_xlsx.write_to_excel(write_path, self.stock_dates)
                

    def batch_stocks(self):
        length = len(self.stocks)
        part = length // 4
        first = self.stocks[0:part]
        second = self.stocks[part:part * 2]
        third = self.stocks[part * 2:part * 3]
        fourth = self.stocks[part * 3:]
        stk = [first, second, third, fourth]

        for index, batch in enumerate(stk):
            self.run_the_stocks(batch, index)
            self.write_data_txt_excel(index)
            time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--INPUT_PATH',
        required=True,
        help='Please type a string for the path where your array of data is located (i.e. "Your_Path/stocks.txt" )')
    parser.add_argument(
        '--OUTPUT_PATH',
        required=True,
        help='Please type a string for the path where to output (i.e. "Your_Path/write/" )')
    parser.add_argument(
        '--TEXT_FILE',
        required=False,
        help='Type True if you want to output to txt file otherwise will write to excel file')

    args = parser.parse_args()
    zacks_scraper = Zacks_Scraper(args.INPUT_PATH, args.OUTPUT_PATH, args.TEXT_FILE)
    zacks_scraper.batch_stocks()
