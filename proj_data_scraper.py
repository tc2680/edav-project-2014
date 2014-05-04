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
    html_str = 'Past Quarterly Returns (%) for '+ symbol_str
    #----------------------------------------------- 
    # for window sample
    #url = "file:///C:/UserTemp/tchen/Profession/Columbia%20University/W4701%20-%20Exploratroy%20data%20analysis%20&%20visualization/project/Local%20Test%20Yahoo%20Finance.html"
    #----------------------------------------------- 
    # for mac sample
    #url = 'file:///Users/tommiechen/Desktop/Columbia%20University/W4701%20-%20Exploratroy%20Data%20Analysis/project/Local%20Test%20Yahoo%20Finance.html'
    #----------------------------------------------- 
    # for live
    yahoo_url = "http://finance.yahoo.com/q/pm?s=" + symbol_str + "+Performance"
    url = yahoo_url 
    
    page = urlopen(url)
    soup_package = BeautifulSoup(page)
    page.close()
    
    #----------------------------------------------- 
    #   find the very top table definition yfncsumtab
    #----------------------------------------------- 
    all_books_table = soup_package.find("table", id="yfncsumtab")
    
    #----------------------------------------------- 
    #    find html table for "Past Quarterly Returns (%) for FBIOX"
    #----------------------------------------------- 
    int_count = 0
    target_table_no = 0
    all_module_title = all_books_table.find_all("span", class_="yfi-module-title")
    for module_title in all_module_title:
        #print("module_title", int_count, module_title.string) # print real table names
        if(module_title.string==html_str): #"Past Quarterly Returns (%) for FBIOX"
            target_table_no = int_count
    #        print( soup.find_all(text=html_str)[0].parent.parent.parent.parent )
    #        print(int_count, module_title)
        int_count += 1
    #print("found target table no at %i" % (target_table_no)) # show which table we're interested
    
    #----------------------------------------------- 
    #    find content of target table 
    #----------------------------------------------- 
    int_count = 0
    target_table_html = ""
    all_data_table = soup_package.find_all("table", class_="yfnc_datamodoutline1")
    for table_title in all_data_table:
        if(int_count==target_table_no):
            target_table_html = table_title
    #        print("----> \n", int_count, target_table_html)
        int_count += 1
    #print("found target html block\n", target_table_html)
    
    #----------------------------------------------- 
    #   define output data array
    #----------------------------------------------- 
    #data_array = list(list("" for i in range(5)) for j in range(10)) # one way to create an array
    number_column = 6 #(symbol, year, q1, q2, q3, q4)
    number_row = 1 # set starting from "1" reserved for header row
    #----------------------------------------------- 
    def make_list(size):
        mylist = []
        for i in range(size):
            mylist.append("")
        return mylist
    #----------------------------------------------- 
    def make_matrix(rows, cols):
        matrix = []
        for i in range(rows):
            matrix.append(make_list(cols))
        return matrix
    #----------------------------------------------- find # of rows
    all_column_label = target_table_html.find_all("td", attrs={"class":"yfnc_datamodlabel1"} )
    for column_label in all_column_label:
        number_row += 1
    #----------------------------------------------- create output array
    data_array = make_matrix(number_row, number_column)    
    
    #----------------------------------------------- 
    #   find first row as column header
    #----------------------------------------------- 
    if(insert_header):
        all_column_title = target_table_html.find_all("td", attrs={"class":"yfnc_tablehead1"} )
        #----------------------------------------------- 
        data_array[0][0] = "symbol"
        data_array[0][1] = "year"
        int_count = 1
        for column_title in all_column_title:
            if(int_count==1):
                data_array[0][int_count] = "year"
            else:
                data_array[0][int_count] = column_title.string
        #    print(int_count, column_title.string)
            int_count += 1
        #print(data_array)
    
    #----------------------------------------------- 
    #    find succeeding data
    #----------------------------------------------- 
    #----------------------------------------------- year column
    all_column_label = target_table_html.find_all("td", attrs={"class":"yfnc_datamodlabel1"} )
    int_count = 1 # "1" reserved for header row
    for column_label in all_column_label:
        data_array[int_count][0] = symbol_str    
        data_array[int_count][1] = column_label.string
        int_count += 1
    #print(data_array)
    #----------------------------------------------- quarter return column
    all_column_data = target_table_html.find_all("td", attrs={"class":"yfnc_datamoddata1"})
    data_column = 5 # there are 4 quarters per year (column indexes are 2, 3, 4, 5) 
    data_row = 1 # "1" is reserved for header row
    int_data_count = 2 # "0" for symbol column, "1" year column
    for column_data in all_column_data:
        data_array[data_row][int_data_count] = column_data.string
    #    print(data_row, int_data_count, column_data.string)
        if int_data_count == data_column: 
            int_data_count = 2 # reset
            data_row += 1
        else:
            int_data_count += 1
    #print(data_array)
    
    #----------------------------------------
    #   write to output file
    #----------------------------------------
    #with open("output.txt", "w") as fp: #write a new text file
    with open("output.csv", "a") as fp: #append text to file
        fp.writelines("%s\n" % ",".join(items) for items in data_array) # ok line
        
        
#----------------------------------------------- 
#   symbol and run for live
#-----------------------------------------------
insert_header = True
#symbol_file = "master-symbol-list.csv" # live
symbol_file = "master-symbol-list-test.csv" # test
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
#scraper_function("FBIOX")
