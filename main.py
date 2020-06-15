import requests
from bs4 import BeautifulSoup as BS
import re
from time import sleep
import time
import vk_api
import vk
import pymysql.cursors
from adds import connect
import os
#Узнаем будущие матчи и сейчашние
token = '8f8b935dbc09eab696c9e1b710c8bd99bbd6be6460f4177efcedac4af43f237908f17329e983683a168b8'
connection = connect()
vk = vk_api.VkApi("+375336671825", "KoLeRiNo")
vk.auth()
while True:

    timematch = time.strftime ( "%Y-%m-%d - %A" ) #Сегодняшний день в оформлении hltv.org
    r = requests.get('https://www.hltv.org/matches')
    soup = BS(r.content, 'html.parser') #Парсит данные c ссылки сверху
    teams = []
    #Высчитывает команды которые играю в это день
    for i in soup.findAll('div', class_='match-day'): #Ищет все div с статусом день матча
        if re.search(r''+timematch+'', str(i)) != None: # Проверяет наличие дня с сегодняшней датой . Определяет!!!
            for a in i.findAll('a'): #Выбирает все ссылки с сайта
                result = re.search(r'/matches/', str(a)) #Проверяет ссылку по очереди на ту что с матчем
                if result != None: #Если пооски не пустые, то записываем команду в массив
                    teams.append(a.get('href'))

    # Результаты!
    r = requests.get('https://www.hltv.org/results')
    soup = BS(r.content, 'html.parser') #Парсит данные с ссылки сайта с результатами
    results = []
    for i in soup.findAll('div', class_='results-sublist'): #Ищет все div в результатах
        #if re.search(r'Results for '+time.strftime('%B %d'), str(i)) != None: #Ищет по сегодняшнему дню
        for q in i.findAll('div', class_='result-con'):
            for a in q.findAll('a'): #Ищет все ссылки
                result = re.search(r'matches', str(a)) #Проверяет ссылку на ту что с матчем
                if result != None: #Если поиски не равны ничему, то записываем команду в массив
                    results.append(a.get('href'))
            for a in q.findAll('td', class_='result-score'):
                score = a.text


    for i in teams:
        con = i

        #Узнаем проценты на команду

        #print(i)
    #    timeforsleep += 1
     #   s = requests.get ( 'https://www.hltv.org' + str ( con ) )
     #   soup = BS ( s.content , 'html.parser' )
     #   teampercent = []
     #   for q in soup.findAll('div', class_='percentage'):
      #      teampercent.append(q.text)
      #  team = []
      #  for q in teampercent:
       #     lol = q
       #     team.append(float(lol.replace ( "%" , "" ))) #Для высчитывания победы процентами
      #  teampercent = team

        #Получение названия команды

        s = requests.get ( 'https://www.hltv.org' + str ( con ) )
        soup = BS ( s.content , 'html.parser' ) #Парсим название команды
        teamname = []
        for q in soup.findAll('div', class_='teamName'): #Ищем div с классом teamName
            teamname.append(q.text) #Записываем название команды в массив
        teamstatistick = []

        #Прошлые результаты команд

        #for j in soup.findAll('table', class_='table matches'): #Ищем прошлую статистику команд
            #for q in j.findAll('td', class_='spoiler'):
                #teamstatistick.append(q.text)

        conn = 0
        teamopponent = []
        b = soup.findAll('table', class_='table matches')

        for a in b[0].findAll('tr', class_='table'):
            conn+=1
        for q in b[0].findAll('tr',class_='table'):
            for a in q.findAll ( 'a' ) :
                result = re.search ( r'/team/' , str ( a.get('href') ) )
                if result != None :
                    teamopponent.append ( a )
            for i in q.findAll('td', class_='spoiler'):
                teamstatistick.append(i.text)
        if conn != 5:
            conn = 5 - conn
            for i in range(conn):
                teamstatistick.append("0 - 0")

        conn = 0
        for a in b[1].findAll('tr', class_='table'):
            conn+=1
        for q in b[1].findAll('tr', class_='table'):
            for a in q.findAll('a'):
                result = re.search(r'/team/', str(a))
                if result != None:
                    teamopponent.append(a)
            for i in q.findAll('td', class_='spoiler'):
                teamstatistick.append(i.text)
        if conn != 5:
            conn = 5 - conn
            for i in range(conn):
                teamstatistick.append("0 - 0")
        print(teamname)
        print(teamstatistick)
        #print(teamopponent)

        opponents = []
        for q in teamopponent:
            opponents.append(q.get('href'))


        teamopponents = []
        ic = 0
        for q in opponents: #Для каждого соперника из массива с ссылками
            con1 = q # con1 равно q
            s = requests.get ( 'https://www.hltv.org' + str ( con1 ) )
            soup = BS ( s.content , 'html.parser' ) #Парсим эту команду
            for a in soup.findAll ( 'div', class_="profile-team-stat" ): #Для каждого div с статистикой команды
                for b in a.findAll('span', class_='right'): #Рейтинг
                    resultx = re.search ( r'-' , str ( b.text ) ) #Проверяет на наличие в рейтинге
                    if resultx != None: # Если НЕ в рейтинге
                        teamopponents.append ( '100' ) #То рейтинг 100
                        ic += 1 #считает что то
                        if ic == 11 :
                            del teamopponents [ 10 ]
                            ic -= 1
                    else: # Если в рейтинге
                        result = re.search ( r'/ranking/teams' , str ( b ) ) #Поиск ссылки на рейтинг
                        if result != None : #Если она есть то
                            result = re.search ( r'#' , str(b.text ) ) #Еще одна проверка на наличие рейтинга
                            if result != None : #Удачно
                                opponent = (b.text).replace ( "#" , "" )
                                teamopponents.append(opponent)
                                ic += 1
                                if ic == 11:
                                    del teamopponents[10]
                                    ic -= 1
        #print(teamopponents)

        s = requests.get ( 'https://www.hltv.org' + str ( con ) )
        soup = BS ( s.content , 'html.parser' )
        #Получение ссылки на 2 команды:
        teamslink = []
        for q in soup.findAll('a'):
            result = re.search(r'/team/', str(q))
            if result != None:
                teamslink.append(q.get('href'))
        #print(teamslink)
        #1
        if teamslink != []:
            if teamslink[0] != teamslink[1]:
                s = requests.get( 'https://www.hltv.org' + teamslink[0])
                soup = BS (s.content , 'html.parser')
                for a in soup.findAll ( 'div', class_="profile-team-stat" ) :
                    for b in a.findAll('span', class_='right'):
                        resultx = re.search ( r'-' , str ( b.text ) )
                        if resultx != None:
                            teamtopone = '100'
                        else:
                            result = re.search ( r'/ranking/teams' , str ( b ) )
                            if result != None :
                                result = re.search ( r'#' , str(b.text ) )
                                if result != None :
                                    teamtopone = (b.text).replace ( "#" , "" )
        #2
                s = requests.get( 'https://www.hltv.org' + teamslink[1])
                soup = BS (s.content , 'html.parser')
                for a in soup.findAll ( 'div', class_="profile-team-stat" ) :
                    for b in a.findAll('span', class_='right'):
                        resultx = re.search ( r'-' , str ( b.text ) )
                        if resultx != None:
                            teamtoptwo = '100'
                        else:
                            result = re.search ( r'/ranking/teams' , str ( b ) )
                            if result != None :
                                result = re.search ( r'#' , str(b.text ) )
                                if result != None :
                                    teamtoptwo = (b.text).replace ( "#" , "" )
        #Результаты!
        #resultname
        baslist = []
        with connection.cursor () as cursor :
            row = cursor.execute(f"SELECT Gmatch FROM matches WHERE 1 ")
            for q in range(row):
                qq = cursor.fetchone()
                for i,a in qq.items():
                    baslist.append(a)
        #print(baslist)
        reslist = []
        for r in results:

            s = requests.get( 'https://www.hltv.org' +r)
            soup = BS(s.content, 'html.parser')
            for q in soup.findAll ( 'div' , class_='teamName' ) :
                reslist.append ( q.text )

            if (reslist[0]+'-'+reslist[1]) in baslist:
                with conection.cursor () as cursor :
                    cursor.execute(f"SELECT answer FROM matches WHERE Gmatch = '{reslist[0]+'-'+reslist[1]}'")
                    qq = cursor.fetchone()
                    for i,a in qq.items():
                        answer = a
                    if answer == 1:
                        score = re.split('-', score)
                        if score[0] > score[1]:
                            cursor.execute ( f"DELETE FROM matches WHERE Gmatch = '{reslist[0]+'-'+reslist[1]}'" )
                            connection.commit()
                            vk.method ( "wall.post" , {"from_group" : 1 , "owner_id" : -154885097 , "message" : "[БОТ] Победа!\n"
                                                                                                                "Команда "+relist[0]+" одержала победу над "+relist[1]+" со счетом "+score[0]+"-"+score[1]+"\n"} )
                    elif answer == 2:
                        score = re.split('-',score)
                        if score[0] < score[1]:
                            cursor.execute( f"DELETE FROM matches WHERE Gmatch = '{reslist[0]+'-'+reslist[1]}'")
                            connection.commit()
                            vk.method ( "wall.post" , {"from_group" : 1 , "owner_id" : -154885097 , "message" : "[БОТ] Победа!\n"
                                                                                                                "Команда "+relist[1]+" одержала победу над "+relist[2]+" со счетом "+score[1]+"-"+score[0]+"\n"} )

        #Получение времени
        timenow = time.strftime("%H:%M")
        s = requests.get( 'https://www.hltv.org' + str(con))
        soup = BS (s.content , 'html.parser')
        timer = ""
        for q in soup.findAll('div', class_= 'timeAndEvent'):
            timer = q.select('.time')
            #print(timer[0].text)
            timer = timer[0].text
        #print(timer.replace(time.strftime("%H:"), ""))
        result = re.split(r':',timer,maxsplit=1)
        rusult = re.split(r':',timenow,maxsplit=1)
        #print(result,rusult)
        #print ( str ( teamname [ 0 ] ) + "-" + str ( teamname [ 1 ] ) )

        timecode = 3
        if int(rusult[0]) + timecode > 24:
            rusult1 = int(rusult[0])-21
        else:
            rusult1 = int(rusult[0])+timecode
        if int ( result [ 0 ])  == rusult1 :
            with connection.cursor() as cursor :
                resultx = cursor.execute(f"SELECT Gmatch FROM `matches` WHERE Gmatch = '{str ( teamname [ 0 ] ) + '-' + str ( teamname [ 1 ] )}' ")
                if resultx < 1:
                    cursor.execute(f"INSERT INTO `matches`(`Gmatch`) VALUES ('{str ( teamname [ 0 ] )  +'-'+ str ( teamname [ 1 ] )}')")
                    connection.commit()
                    text = ""
                    #if teampercent [ 1 ] - teampercent [ 0 ] > 0 :
                     #   text = text + str ( teamname [ 1 ] )
                    #else :
                     #   text = text + str ( teamname [ 0 ] )
                    ic = 0
                    teamonestatistic = int(teamtopone)/100
                    teamtwostatistic = int(teamtoptwo)/100
                    for i in range(10):
                        result = re.split(r' - ', teamstatistick[i],maxsplit=1)
                        if i < 5:
                            if int(result[0]) > int(result[1]):
                                teamonestatistic = teamonestatistic - (int(teamtopone)/int(teamopponents[i]))
                            else:
                                teamonestatistic = teamonestatistic + (int(teamopponents[i])/int(teamtopone))
                        else:
                            if int ( result [ 0 ] ) > int ( result [ 1 ] ) :
                                teamtwostatistic = teamtwostatistic - (int ( teamtoptwo )/int ( teamopponents [ i ] ))
                            else :
                                teamtwostatistic = teamtwostatistic + (int ( teamopponents [ i ] )/int ( teamtoptwo ))
                    if teamonestatistic < teamtwostatistic:
                        cursor.execute(f"UPDATE matches SET answer = 1 WHERE Gmatch = '{teamname[0]+'-'+teamname[1]}'")
                        connection.commit()
                        text = text + str(teamname[0])
                    else:
                        cursor.execute (f"UPDATE matches SET answer = 2 WHERE Gmatch = '{teamname [ 0 ] + '-' + teamname [ 1 ]}'" )
                        connection.commit()
                        text = text + str(teamname[1])

                    print ( "[БОТ] Приближается матч между "+teamname[0]+" и " + teamname [ 1 ] + "\nОжидаемо, что выйграют " + text )
                    vk.method("wall.post", {"from_group": 1, "owner_id": -154885097, "message": "[БОТ] Приближается матч между "+teamname[0]+" и " + teamname [ 1 ] + "\nОжидаемо, что выйграют " + text})
        #print(time.strftime("%Y-%m-%d - %A"))


        #Итоги в 1:00
       # s = requests.get( 'https://www.hltv.org/results' )
       # soup = BS (s.content , 'html.parser')
       # for q in soup.findAll('div', class_='results-sublist'):
           # result = re.search( time.strftime("Results for %B %d"), str(q))
           # if result != None:
                #print(q)

    #Классно


