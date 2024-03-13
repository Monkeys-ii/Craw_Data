import requests
from bs4 import BeautifulSoup
import json
import pymongo
import time
import schedule


def ConvertToJson(Time, Country, Flag, Cash_money, Transfer_money, Sell_money) :

    data_json = {
        "Time" : Time,
        "Country" : Country,
        "Flag" : Flag,
        "Cashmoney" : Cash_money,
        "Transfermoney" : Transfer_money,
        "Sellmoney" : Sell_money
    }

    return data_json



def Get_Request() :
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url = 'https://www.vietcombank.com.vn/KHCN/Cong-cu-tien-ich/Ty-gia', headers = headers)
    xuly = BeautifulSoup(r.text, 'html.parser')
    data = xuly.find_all('ul', {'class' : 'dropdown-options-wrapper'})
    return data, xuly


def LinkDatabase() :
    # Link DataBase
    client = pymongo.MongoClient("mongodb://localhost:27017/") # Ket noi voi database MongoDB
    db = client["News"]  # Ten database
    collection = db["NewsAndLink"] # Ten collection
    return collection


def XuLy() :  
    data, xuly = Get_Request() 
    li_data = str(data[0].find_all('li', {'class' : 'dropdown-options__item'}))
    Li_data = li_data.split(',')
    Li_data[len(Li_data) - 1] = Li_data[len(Li_data) - 1][: len(Li_data[len(Li_data) - 2])]
    Li_data[0] = Li_data[0][1 :]

    day_update = (xuly.find_all('strong'))  # Ngay va gio update
    day = str(day_update[0])[9 : 30]

    return Li_data, day

def XoaDuLieuCu() :
    result = LinkDatabase()
    result.delete_many({})


def XuLyData() :
    Li_data, day = XuLy()
    collection = LinkDatabase()

    name_money =    ['US DOLLAR', 'EURO', 'POUND STERLING', 'YEN', 'AUSTRALIAN DOLLAR', 'SINGAPORE DOLLAR', 'THAILAND BAHT', 'CANADIAN DOLLAR',\
                'SWISS FRANC', 'HONGKONG DOLLAR', 'YUAN RENMINBI', 'DANISH KRONE', 'INDIAN RUPEE', 'KOREAN WON', \
                'KUWAITI DINAR', 'MALAYSIAN RINGGIT', 'NORWEGIAN KRONER', 'RUSSIAN RUBLE', 'SAUDI RIAL', 'SWEDISH KRONA']
    i = 0
    for x in Li_data :
        data = x.split('"')
        country = data[5] + ' ' + name_money[i]
        i += 1
        flag = 'https://www.vietcombank.com.vn/' + data[7] # Flag
        cash_money = data[3]    # Tien mat
        transfer_money = data[13]   # Tien chuyen khoan
        sell_money = data[11]   # Tien ban
        Data_json = ConvertToJson(day, country, flag, cash_money, transfer_money, sell_money)
        collection.insert_one(Data_json)

    
def AutoUpdate() :
    Get_Request()

    LinkDatabase()

    XuLy()

    XoaDuLieuCu()

    XuLyData()

schedule.every(1).minutes.do(AutoUpdate)
i = 0
if __name__ == '__main__' :
    while(True) :
        
        schedule.run_pending()
        print(i)
        i += 1
        time.sleep(2)
