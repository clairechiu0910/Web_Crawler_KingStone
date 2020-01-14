import urllib.request
from bs4 import BeautifulSoup
import sys
import logging

from datetime import date
from datetime import timedelta

def setNextTime(RankType, cur_date):
    if RankType == "week":
        return cur_date + timedelta(days = 7)
    if RankType == "month":
        if cur_date.month == 12:
            return date(cur_date.year+1, 1, cur_date.day)
        else:
            return date(cur_date.year, cur_date.month+1, cur_date.day)
    if RankType == "year":
        return date(cur_date.year+1, cur_date.month, cur_date.day)

def setUrl(class_id, RankType, cur_date, page):
    if RankType == "week":
        return str("https://www.kingstone.com.tw/bookold/book_board.asp?" + "Selltype=sell01" + "&class_id=" + class_id + "&RankType=week" + 
                "&W_Type=" + str(cur_date.year) + "/" + str(cur_date.month) + "/" + str(cur_date.day) + "&page=" + str(page))
    if RankType == "month":
        return str("https://www.kingstone.com.tw/bookold/book_board.asp?" + "selltype=sell01" + "&class_id=" + class_id + "&RankType=month" + 
                "&YM_Type=" + str(cur_date.year) + "&M_Type=" + str(cur_date.month) + "&page=" + str(page))
    if RankType == "year":
        return str("https://www.kingstone.com.tw/bookold/book_board.asp?" + "selltype=sell01" + "&class_id=" + class_id + "&RankType=year" + 
                "&YM_Type=" + str(cur_date.year) + "&page=" + str(page))

def toSunday(cur_date):
    sun_date = cur_date + (timedelta(days = 6 - cur_date.weekday()))
    return sun_date

def collect_data_week(class_id, RankType, start_date, end_date):
    cur_date = start_date
    cur_date = toSunday(cur_date)
    if start_date > end_date:
        print("date error")
        exit()

    while(cur_date <= end_date):
        print(cur_date.year, cur_date.month, cur_date.day)

        if cur_date.month < 10:
            file_title_abs = open('./data_title_abs/' + str(cur_date) + '_title_abs.txt', 'w', encoding = 'utf-8') #windows default: utf-8
        else:
            file_title_abs = open('./data_title_abs/' + str(cur_date) + '_title_abs.txt', 'w', encoding = 'utf-8') #windows default: utf-8

        for page in range(1, 11):
            url = setUrl(class_id, RankType, cur_date, page)

            for test_connect in range(10):
                try:
                    web_pt = urllib.request.urlopen(url, timeout = 10)
                except TimeoutError:
                    logging.error('socket.timeout: The read operation timed out: ' + url)
                    continue
                except:
                    logging.error("other error happened: " + url)
                    continue
                if(web_pt.getcode() == 200): break
            if(web_pt.getcode() != 200): 
                print("cannot connect to the website")
                exit()        

            html_code = web_pt.read()
            del  web_pt
            soup = BeautifulSoup(html_code, 'lxml')
            a_titles = soup.find_all('a', 'anchor')
            p_texts = soup.find_all('p')

            for j in range(len(a_titles)):
                if(j<10):
                    file_title_abs.write("@book_index: " + str(j+1 + (page-1)*10) + '\n')
                    file_title_abs.write("@book_title:\n")
                    file_title_abs.write(a_titles[j].get_text() + '\n')
                    file_title_abs.write("@book_abstract:\n")
                    file_title_abs.write(p_texts[j].get_text() + '\n')

        file_title_abs.close()

        cur_date = setNextTime(RankType, cur_date)
