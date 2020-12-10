import requests
from bs4 import BeautifulSoup as BS
import re
from time import sleep
import time
#import vk_api
#import vk
from boto.s3.connection import S3Connection
import os
from fake_useragent import UserAgent
import telebot
import sqlite3
UserAgent().chrome
print("Бот запущен")
conn = sqlite3.connect("server.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
# Создание таблицы

#cursor.execute(f"""INSERT INTO bot VALUES ('SASKE')""")

#print(cursor.execute(f"SELECT game FROM bot WHERE game = '333'").fetchone())
def bdinsert(what):
    if cursor.execute(f"SELECT game FROM bot WHERE game = '{what}'").fetchone() == None:
        cursor.execute(f"""INSERT INTO bot VALUES ('{what}')""")
        return None
    else:
        return 1
    conn.commit()

def register(what):
	try:
		result = cursor.execute(f"SELECT * FROM bot WHERE game='{what}'")
		row = cursor.fetchone()
		if result == 0:
			cursor.execute(f"INSERT INTO bot(game) VALUES('{what}')")
			conn.commit()
		else:
			return row
	finally:
		conn.commit()

#print(cursor.execute("SELECT * FROM bot").fetchall())
bot = telebot.TeleBot("1486092253:AAFVMoBeQ5MTKL0kNSiCocp7dVmayYPwNoY")
#response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})


def main():
    timematch = time.strftime ( "%A - %Y-%m-%d" )  # Сегодняшний день в оформлении hltv.org
   # timematch = time.strftime ( "%A - %Y-%m-10" )  # Сегодняшний день в оформлении hltv.org
    #print(timematch)


    teams = [ ]

    # Высчитывает команды которые играю в это день
    r = requests.get ( 'https://www.hltv.org/matches' , headers={'User-Agent' : UserAgent ().chrome} )
    soup = BS ( r.content , 'html.parser' )  # Парсит данные c ссылки сверху

    for i in soup.findAll ( 'div' , class_='upcomingMatchesSection' ) :  # Ищет все div с статусом день матча
        if re.search ( r'' + timematch + '' , str ( i ) ) != None : # Проверяет наличие дня с сегодняшней датой . Определяет!!!
            for a in i.findAll( 'a', class_='matchAnalytics' ) :  # Выбирает все ссылки с сайта
                result = re.search ( r'/betting' , str ( a ) )  # Проверяет ссылку по очереди на ту что с матчем
                if result != None and len(teams) != 7:  # Если пооски не пустые, то записываем команду в массив
                    teams.append ( a.get ( 'href' ) )
    print(teams)
    if teams != []:
        for i in teams:
            print(i)
            c = True
            stats = [ ]
            maps = [ ]
            name = [ ]
            r = requests.get ( 'https://www.hltv.org'+i , headers={'User-Agent' : UserAgent ().chrome} )
            soup = BS (r.content, 'html.parser')
            col = -1

            for i in soup.findAll('td', class_='table-event'):
                col += 1
                if '-' == i.text:
                    stats.append("0.88")
                    c = False
                else:
                    stats.append(i.text)
            col = 0
            for i in soup.findAll('div', class_="analytics-handicap-map-data"):
                for a in i.findAll('div', class_=""):
                    if re.findall('\D', a.text) == ['.']:
                        if col == 0:
                            maps.append(a.text)
                            col += 1
                        else:
                            col = 0

            for i in soup.findAll('div', class_='name'):
                name.append(i.text)
            if len(stats) > 10:
                while len(stats) != 10:
                    stats.pop(10)
            print(stats)

            if len(stats) == 0:
                main()
            
            try:
                dstats1 = (float(stats[0]) + float(stats[1]) + float(stats[2]) + float(stats[3]) + float(stats[4]))/5
                dstats2 = (float(stats[5]) + float(stats[6]) + float(stats[7]) + float(stats[8]) + float(stats[9]))/5
                #for i in stats(range(5)):
                 #   dstats1 = dstats + int(i)
                #dstats2 = sum(int(stats[5]), int(stats[6]), int(stats[7]), int(stats[8]), int(stats[9]))/5
                #dstats1 = sum(int(stats[0]), int(stats[1]), int(stats[2]), int(stats[3]), int(stats[4]))/5
                #dmat1 = float ( maps [ 0 ] )*dstats1
                #dmat2 = float ( maps [ 1 ] )*dstats2
                match = name [ 0 ] + " - " + name [ 1 ]
            except Exception:
                print("Случился краш")
                sleep(15)
                main()
            print(match)
            cursor.execute(f"SELECT * FROM bot")

            kok = len(cursor.fetchall())+1

            try:
                if bdinsert(match) == None and c == True:
                    if dstats1 > dstats2:
                        if register(match) != None:
                            bot.send_message("@mlg_betbot", "#"+str(kok)+" Cтавка от бота:\n" +name[0]+" - "+name[1]+"\n"
                                                                       "Ставка: Победа "+name[0])


                    elif dstats1 < dstats2:
                        if register(match) != None:
                            bot.send_message("@mlg_betbot", "#"+str(kok)+" Cтавка от бота:\n"
                                                +name[0]+" - "+name[1]+"\n"
                                                                       "Ставка: Победа "+name[1])
            except Exception:
                print("Ошибка с выводом данных")
            finally:
                print("+")
            print(dstats1, dstats2)
            #print (dmat1,dmat2 )
            print("------------------------------")
        #print(len(stats))





while __name__ == '__main__':
    main()
    sleep(120)
