import requests
from bs4 import BeautifulSoup as BS
import re
from time import sleep
import time
import vk_api
import vk
from boto.s3.connection import S3Connection
import os
from fake_useragent import UserAgent
import telebot
import sqlite3
UserAgent().chrome

conn = sqlite3.connect(":memory:") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
# Создание таблицы
cursor.execute("""CREATE TABLE bot
                  (game text)
               """)

#cursor.execute(f"""INSERT INTO bot VALUES ('SASKE')""")

#print(cursor.execute(f"SELECT game FROM bot WHERE game = '333'").fetchone())
def bdinsert(what):
    if cursor.execute(f"SELECT game FROM bot WHERE game = '{what}'").fetchone() == None:
        cursor.execute(f"""INSERT INTO bot VALUES ('{what}')""")
        print("none")
        return None
    else:
        print("1")
        return 1
        
    conn.commit()
#print(cursor.execute("SELECT * FROM bot").fetchall())
bot = telebot.TeleBot("1486092253:AAFVMoBeQ5MTKL0kNSiCocp7dVmayYPwNoY")
#response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})


def main():

    timematch = time.strftime ( "%A - %Y-%m-%d" )  # Сегодняшний день в оформлении hltv.org
    #print(timematch)


    teams = [ ]

    # Высчитывает команды которые играю в это день
    r = requests.get ( 'https://www.hltv.org/matches' , headers={'User-Agent' : UserAgent ().chrome} )
    soup = BS ( r.content , 'html.parser' )  # Парсит данные c ссылки сверху

    for i in soup.findAll ( 'div' , class_='upcomingMatchesSection' ) :  # Ищет все div с статусом день матча
        if re.search ( r'' + timematch + '' , str ( i ) ) != None : # Проверяет наличие дня с сегодняшней датой . Определяет!!!
            for a in i.findAll( 'a', class_='matchAnalytics' ) :  # Выбирает все ссылки с сайта
                result = re.search ( r'/betting' , str ( a ) )  # Проверяет ссылку по очереди на ту что с матчем
                if result != None  and len(teams) != 7:  # Если пооски не пустые, то записываем команду в массив
                    teams.append ( a.get ( 'href' ) )

    if teams != []:
        for i in teams:
            stats = [ ]
            maps = [ ]
            name = [ ]
            r = requests.get ( 'https://www.hltv.org'+i , headers={'User-Agent' : UserAgent ().chrome} )
            soup = BS (r.content, 'html.parser')
            col = -1
            for i in soup.findAll('td', class_='table-event'):
                col += 1
                if '-' == i.text:
                    stats.append("1")
                    #stats.append(soup.findAll('td', class_='table-3-months')[col].text)
                else:
                    stats.append(i.text)
            col = 0
            #print(stats)
            #stats = ['1.12', '1.08', '1.00', '0.99', '0.97', '1.11', '1.09', '1.09', '1.08', '0.97']
            for i in soup.findAll('div', class_='analytics-handicap-map-data'):
                for a in i.findAll('div', class_=""):
                    if re.findall('\D', a.text) == ['.']:
                        if col == 0:
                            maps.append(a.text)
                            col += 1
                        else:
                            col = 0
            #maps = ['-','10.23']
            for i in soup.findAll('div', class_='name'):
                name.append(i.text)
            print(name)
            #print(stats)
            #print ( teams )
            if len(stats) > 10:
                while len(stats) != 10:
                    stats.pop(10)
            if len(stats) == 0:
                main()
        #print(stats)
        #else:
          #  sleep(1)
           # main()

            try:
                dstats1 = (float(stats[0]) + float(stats[1]) + float(stats[2]) + float(stats[3]) + float(stats[4]))/5
                dstats2 = (float(stats[5]) + float(stats[6]) + float(stats[7]) + float(stats[8]) + float(stats[9]))/5
                dmat1 = float ( maps [ 0 ] )*dstats1
                dmat2 = float ( maps [ 1 ] )*dstats2
                match = name [ 0 ] + " - " + name [ 1 ]
            except Exception:
                sleep(15)
                main()


            try:
                if bdinsert(match) == None:
                    if dstats1 > dstats2 and dmat1 > dmat2:
                        print("1")
                        bot.send_message("@mlg_betbot", "Cтавка от бота:\n" +name[0]+" - "+name[1]+"\n"
                                                                       "Ставка: Победа "+name[0])


                    if dstats1 < dstats2 and dmat1 < dmat2:
                        print("2")
                        bot.send_message("@mlg_betbot", "Cтавка от бота:\n"
                                                +name[0]+" - "+name[1]+"\n"
                                                                       "Ставка: Победа "+name[1])

            finally:
                print("")
            print(dstats1, dstats2)
            print (dmat1,dmat2 )
            print("------------------------------")
        #print(len(stats))
    sleep(120)




while __name__ == '__main__':
    main()
