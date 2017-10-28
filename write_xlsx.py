from ast import literal_eval
from time import sleep
from datetime import datetime, date
import xlrd, xlsxwriter, pprint

def prep_tickers(path):
	with open(path, 'r') as myfile:
	    data=myfile.read().replace('\n', '')

	stocks = literal_eval(data)
	return stocks

def write_data(part, stocks):
	write_path = '/Your/path/data/stocks_dates_%s.txt' % (part)
	open(write_path, 'w').close()
	with open(write_path, 'r+') as g:
		g.write(str(stocks))

def get_universe(stock_universe={}):
	parts = ['0', '1', '2', '3']

	for part in parts:
		path = '/Your/path/data/stocks_dates_%s.txt' % (part)
		cur_stocks = prep_tickers(path)
		for stock in cur_stocks:
			if stock not in stock_universe:
				stock_universe[stock] = cur_stocks[stock]

	return stock_universe

def write_to_excel(xlsx_path, stocks_dates):
	workbook = xlsxwriter.Workbook(xlsx_path)
	worksheet = workbook.add_worksheet()
	row = 0
	for name in stocks_dates:
		col = 0
		worksheet.write(row, col, name)
		col += 1
		for pair in stocks_dates[name]:
			val = '%s, %s' % (pair[0].replace('"', ''), pair[1].replace('"', ''))
			worksheet.write(row, col, val)
			col += 1
		row += 1

	workbook.close()

def prep_stock_dates(dates):
	dates_final = []
	def increment_date(date):
		leap_year_feb = ['2008', '2012', '2016'] # In leap year febuary goes to 29 days otherwise feb is 28 days
		months = {'1':30, '2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
		date = date.split('/') # ['3', '25', '2013']
		if int(date[1]) >= months[date[0]]: # last day of month, so increment month
			if date[0] == '2':
				if date[2] in leap_year_feb: # check leap year
					month = date[0]
					day = int(date[1]) + 1
					day = str(day)
				else:
					month = int(date[0]) + 1
					month = str(month)
					day = '1'
			else:
				month = int(date[0]) + 1
				month = str(month)
				day = '1'
		else:
			month = date[0]
			day = int(date[1]) + 1
			day = str(day)

		date_f = month + '/' + day + '/' + date[2]
		return date_f

		
	for date in dates:
		date = (date[0].replace('"', ''), date[1].replace('"', ''))
		if date[1] == 'AfterClose':
			date = increment_date(date[0])
			dates_final.append(date)
		elif date[1] == '--':
			continue
		else:
			dates_final.append(date[0])

	if len(dates_final) < 10:
		return 'delete'
	else:
		return dates_final

def write_to_excel_date_only(xlsx_path, stocks_dates):
	workbook = xlsxwriter.Workbook(xlsx_path)
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': 1})
	worksheet.write(0, 0, 'Symbol', bold)
	worksheet.write(0, 1, 'TradeDate', bold)
	row = 1
	for name in stocks_dates:
		dates = prep_stock_dates(stocks_dates[name])
		if dates == 'delete':
			continue
		else:
			for date in dates:
				col = 0
				worksheet.write(row, col, name)
				col += 1
				worksheet.write(row, col, date)
				row += 1

	workbook.close()

# stocks = get_universe()
# write_data('universe', stocks)
# stocks = prep_tickers('/Your/Path/data/stocks_dates_universe.txt')
# path = '/Your/Path/data/stocks_dates_only_universe.csv'
# write_to_excel(path, stocks)
# write_to_excel_date_only(path, stocks)




	
