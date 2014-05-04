from bs4 import BeautifulSoup
from urllib import urlopen
import csv
#import re
#import numpy as np
#import sys

def scraper_function(my_symbol):        
    #----------------------------------------------- 
    #   construct url
    #----------------------------------------------- 
    symbol_str = my_symbol
    html_str = 'Fund Overview'
    #----------------------------------------------- 
    # for window sample
    #url = "file:///C:/UserTemp/tchen/Profession/Columbia%20University/W4701%20-%20Exploratroy%20data%20analysis%20&%20visualization/project/Local%20Test%20Yahoo%20Finance.html"
    #----------------------------------------------- 
    # for mac sample
    #url = 'file:///Users/tommiechen/Desktop/Columbia%20University/W4701%20-%20Exploratroy%20Data%20Analysis/project/Local%20Test%20Yahoo%20Finance.html'
    #----------------------------------------------- 
    # for live
    yahoo_url = "http://finance.yahoo.com/q/pr?s=" + symbol_str + "+Profile"
    url = yahoo_url 
    
    page = urlopen(url)
    soup_package = BeautifulSoup(page)
    page.close()
    
    #----------------------------------------------- 
    #   find the very top table definition 
    #----------------------------------------------- 
    all_data_table = soup_package.find_all("table", class_="yfnc_datamodoutline1")
    '''
    for table_title in all_data_table:
            target_table_html = table_title
            print("----> ", target_table_html)
    '''
    insert_str = symbol_str + ","
    
    #-----------------------------------------------    
    #   category title
    #----------------------------------------------- 
    '''
    fund_overview_table = soup_package.find("td", class_="yfnc_datamodlabel1")
    for row in fund_overview_table:
        print(row)
    '''

    #-----------------------------------------------    
    #   category data (appeared in the 1st occurrence)
    #----------------------------------------------- 
    fund_overview_table = soup_package.find("td", class_="yfnc_datamoddata1")
    for row in fund_overview_table:
        insert_str += row
        #print(row)
    #print insert_str
        
    #----------------------------------------
    #   write to output file
    #----------------------------------------
    output_file = "output_profile.csv"
    #with open(output_file, "w") as fp: #write a new text file
    with open(output_file, "a") as fp: #append text to file
        fp.writelines("%s\n" % (insert_str))

#----------------------------------------------- 
#   symbol and run for live
#-----------------------------------------------
insert_header = True
symbol_file = "master-symbol-list.csv" # live
#symbol_file = "master-symbol-list-test.csv" # test
#-----------------------------------------------
run_symbol_no = 1
with open(symbol_file, 'rb') as f:
    symbol_reader = csv.reader(f)
    for my_symbol in symbol_reader:
        print(run_symbol_no, my_symbol[0])
        run_symbol_no += 1
        try:
            scraper_function(my_symbol[0])
        except Exception:
            pass
        insert_header = False

#---- test
#scraper_function("WISEX")
