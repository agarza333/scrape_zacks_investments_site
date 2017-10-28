### Scrape Zacks
This class will scrape Zacks investment site given an input path with an array of stocks, such as the one found in wilshire_stocks.txt.  It will print a dict of tuples of {'A': ('8/15/2009', 'After Close')} for each stock, into the output path.  This script will batch the number of stocks passed into the script into 4 batches of relatively equal size, and 4 output files. Default output is to an excel file.

#### Example Usage:
python scrape_zacks_earnings_dates.py --INPUT_PATH ./wilshire_stocks.txt --OUTPUT_PATH ./