import requests
from bs4 import BeautifulSoup as BS
import re
from time import sleep
import time
#from boto.s3.connection import S3Connection
import os
from fake_useragent import UserAgent
import telebot
import sqlite3
from adds import connect
import pymysql
from pymysql import cursors
UserAgent().chrome

bot = telebot.TeleBot("1486092253:AAFVMoBeQ5MTKL0kNSiCocp7dVmayYPwNoY")

def main():

########################################## В РАЗРАБОТКЕ ###################################################
    #link = ''
    #input(link)
    teams = []
    bots = []
    ggez = []
    bom = 0
    r = requests.get( 'https://betwinner1.com/ru/live/Football/', headers={'User-Agent' : UserAgent ().random} )
    soup2 = BS (r.content, 'html.parser')
    for i in soup2.findAll('a', class_='c-events__name'):
        bots.append(i.get("href"))
    print(bots)
    for gye in bots:
        lol = ''
        mass = [ ]
        status = ''
        link = gye
        r = requests.get ("https://betwinner1.com/ru/"+ link, headers={'User-Agent' : UserAgent ().random} )
        #r = requests.get ( 'https://betwinner.com/ru/cyber/FIFA/2039638-FIFA-20-4x4-England-Championship/' , headers={'User-Agent' : UserAgent ().chrome} )
        soup = BS ( r.content , 'html.parser' )  # Парсит данные c ссылки сверху

        for i in soup.findAll('span', class_='ls-game__score'):
            mass.append(i.text)
            #print(i.text)
        for i in soup.findAll('div', class_='ls-game__text'):
            status = i.text
        if status != None:
            status = status.replace('\n', '')
            status = status.strip()
        if status == '':
            status = 'Не найден'
        for i in soup.findAll('div', class_='ls-game__name'):
        #if 'Андерлехт' in i.text:
            ban = i.text
            ban = ban.replace('\n', '')
            ban = ban.strip()
            teams.append(ban)
        lol = soup.findAll('meta')
        lol = str(lol[1])
        lol = lol.replace('<meta content="Смотри видеотрансляцию ► BETWINNER1.com и играй в LIVE! Принимаем ставки на футбол: ', '')
        lol = lol.replace(' . Угадай победителя:', '')
        lol = lol.replace('" name="description"/>', '')
        print(lol)

    #print(soup.findAll('div', class_='c-tablo__text'))
    #relust = re.search('bets_p1', str(soup))
    #print(relust)
    #col = 0
    #text = ''
    #for i in str(soup):
       # col+=1
      #  if col >= 95000 and col <= 95500:
     #       text = text + i
    #print(text)
        if status != 'Не найден' and lol != '':
            if re.search('1-й', status) != None:
                time = status.replace('1-й Тайм,прошло ', '')
            elif re.search('2-й', status) != None:
                time = status.replace('2-й Тайм,прошло ', '')
            else:
                time = status.replace('Перерыв,прошло ', '')
                time = time.replace('Игра завершена,прошло ', '')
            time = time.replace(' мин', '')
            #print(time)
            cat = ''
            c = False
            print("mass=="+str(mass)+"\nTime=="+str(time)+"\nmass[0]=="+str(mass[0])+"\nmass[3]")
            if (len(mass) == 6) and ('завершена' in time == False) and (mass[0] != '') and (mass[3] != '') and (time != '') and (mass[2] != '') and (mass[5] != ''):
                if (int(mass[0]) == 0) and (int(mass[3]) == 0) and (int(time) >= 60) and (int(mass[2]) == int(mass[5])) and (int(mass[2]) == 0) and (c == False): #Счет 0-0 и время больше 60 минут
                    cat += 'Тотал 0.5 Б'
                    #print(33)
               # elif (int(mass[0]) != int(mass[3])) and (c == False) and (int(time) >= 65) and (int(mass[2]) == int(mass[5])) and (int(mass[2]) == 0): #Счет 0-1 или 1-0 и время больше 65 минут
                #    cat += 'Тотал '+str((int(mass[0])+int(mass[3])))+'.5 Б'
                    #print(22)
                elif (int(mass[0]) != int(mass[3])) and (c == False) and (int(time) >= 55) and (int(mass[2]) == int(mass[5])) and (int(mass[2]) == 0):#Счет 3М и время 65 минут
                    cat += 'Тотал '+str((int(mass[0])+int(mass[3])))+'.5 Б'
                elif ('жен' in lol) == True and int(time) >= 55 :
                    cat += 'Тотал ' + str ( (int ( mass [ 0 ] ) + int ( mass [ 3 ] )) ) + '.5 Б'
                    #print(11)
    #print(relust)

        if len(mass) == 6 and lol != '':
            print(teams[bom]+' - '+teams[bom+1]+'\nМатч идет со счетом: '+mass[0]+' - '+ mass[3]+ '. \nСчет таймов: '+mass[1]+' - '+mass[4]+' | 1 тайм | '+mass[2]+' - '+mass[5]+" | 2 тайм |\n"
                                                                                                                                              "Статус: "+status+'\n'
                                                                                                                                                               'Ставка: 1% Гол будет забит до '+str((int(time)+15))+' минуты, если проигрыш 4% на '+cat)

        #print(lol in ggez)
        name1 = bom
        name2 = bom+1
        bom += 2
        connection = connect()
        if cat != '':
            if len(mass) == 6 :
                if (lol in ggez) == False:
                    ggez.append(lol)
                    with connection.cursor() as cursor:
                        print(cursor.execute(f"SELECT Gmatch FROM matches WHERE Gmatch = '{lol}'"))
                        if cursor.execute(f"SELECT Gmatch FROM matches WHERE Gmatch = '{lol}'") != 1:
                            cursor.execute(f"INSERT INTO matches(Gmatch) VALUES ('{lol}')")
                            connection.commit()

                            bot.send_message('@mlg_betbot', lol+'\nМатч идет со счетом: '+mass[0]+' - '+ mass[3]+ '. \nСчет таймов: '+mass[1]+' - '+mass[4]+' | 1 тайм | '+mass[2]+' - '+mass[5]+" | 2 тайм |\n"
                                                                                                                                              "Статус: "+status+'\n'
                                                                                                                                                               'Ставка: 1% Гол будет забит до '+str((int(time)+15))+' минуты, если проигрыш 4% на '+cat)

            #elif len(mass) == 4:

                #bot.send_message('@mlg_betbot', teams[0]+' - '+teams[1]+'\nМатч идет со счетом: '+mass[0]+' - '+ mass[2]+ '. \nСчет таймов: '+mass[1]+' - '+mass[3]+' | 1 тайм |\n'+
#                                                                                                                                             "Статус: "+status+'\n'
 #                                                                                                                                                              'Ставка: '+cat)


       # teams.append('https://betwinner.com/ru/' + i.get('href'))
    #for i in teams:
     #   k = requests.get( i, headers={'User-Agent' : UserAgent ().chrome} )
      #  soupu = BS ( k.content , 'html.parser' )  # Парсит данные c ссылки сверху
        #print(i)
        #print(soupu)
       # for b in soupu.findAll('span', class_='timer'):
        #    print(b.text)
    #for i in soup.findall('div', data-name="dashboard-champ-content"):
     #   for a in i.findAll('div', class_='c-events-scoreboard__line'):
      #      #print(a)
        #    for b in a.findAll('span', class_='c-events-scoreboard__cell c-events-scoreboard__cell--all'):
       #        print(b.text)
         #   for b in i.find('span', class_="c-events__teams"):
     #           print(b.text)

        #a = requests.get ( 'https://betwinner.com/ru/' + i.get('href') , headers={'User-Agent' : UserAgent ().chrome} )
        #soupu = BS ( a.content , 'html.parser' )  # Парсит данные c ссылки сверху\
    #    print ( soupu )
     #   for i in soupu.findAll('div', class_='score'):
      #      print(i.text)
    print ( "------------------------------" )
    sleep(60)
    #print(1)









#donotcache = 146845136
#password = 'Nt49fh184f'
#username = '001png'
#rsatimestamp = '64000000'
#phone_cod = input ( 'Введите код с мобильного:  ' )
#url = 'https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Ftradeback.io%2Fauth%2Fsteam%2Fhandle&openid.realm=https%3A%2F%2Ftradeback.io&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select'
#print ( url.find ( 'captchaImg' ) )
#dann = {
    #'password' : password ,
   # 'username' : username ,
  #  'twofactorcode' : phone_cod ,
 #   'rsatimestamp' : rsatimestamp ,
 #   'remember_login' : 'true'
#}

#r = S.post ( url , dann )  # >тправка пост запроса)
#print ( r.url )
#result = r.text
#print ( r.text )
#reg = re.search ( 'false' , r.text )
#print ( reg )

#if reg == None :
#    print ( 'GOOD!!!' )
#else :
   # print ( 'BAD!!' )













while __name__ == '__main__':
    main()