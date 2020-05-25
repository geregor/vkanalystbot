import requests
from bs4 import BeautifulSoup as BS
import re
from time import sleep
import time
import vk_api
import vk
import pymysql.cursors
from adds import connect
#Узнаем будущие матчи и сейчашние
token = '8f8b935dbc09eab696c9e1b710c8bd99bbd6be6460f4177efcedac4af43f237908f17329e983683a168b8'

vk = vk_api.VkApi("+375336671825", "KoLeRiNo")
vk.auth()

while True:

    timematch = time.strftime ( "%Y-%m-%d - %A" )
    r = requests.get('https://www.hltv.org/matches')
    soup = BS(r.content, 'html.parser')
    teams = []
    #Высчитывает команды которые играю в это день
    for i in soup.findAll('div', class_='match-day'): #Ищет все div с статусом день матча
        if re.search(r''+timematch+'', str(i)) != None: # Проверяет наличие дня с сегодняшней датой . Определяет!!!
            for a in i.findAll('a'):
                result = re.search(r'/matches/', str(a))
                if result != None:
                    teams.append(a.get('href'))
    #Узнаем проценты на команду
    for i in teams:
        con = i
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
       #     team.append(float(lol.replace ( "%" , "" )))
      #  teampercent = team
        #Получение названия команды
        s = requests.get ( 'https://www.hltv.org' + str ( con ) )
        soup = BS ( s.content , 'html.parser' )
        teamname = []
        for q in soup.findAll('div', class_='teamName'):
            teamname.append(q.text)
        teamstatistick = []
        for q in soup.findAll('td', class_='spoiler'):
            #print(q.text)
            teamstatistick.append(q.text)
        #print(teamstatistick)
        #print(str(teamname))
        teamopponent = []
        for q in soup.findAll('a', class_='text-ellipsis'):
            result = re.search(r'/team/', str(q))
            if result != None:
                teamopponent.append(q)
        if teamstatistick != []:
            del teamopponent[0]
            del teamopponent[0]
        opponents = []
        for q in teamopponent:
            #print(q.get('href'))
            opponents.append(q.get('href'))
        teamopponents = []
        ic = 0
        for q in opponents:
            con1 = q
            s = requests.get ( 'https://www.hltv.org' + str ( con1 ) )
            soup = BS ( s.content , 'html.parser' )
            for a in soup.findAll ( 'div', class_="profile-team-stat" ) :
                for b in a.findAll('span', class_='right'):
                    resultx = re.search ( r'-' , str ( b.text ) )
                    if resultx != None:
                        teamopponents.append ( '100' )
                        ic += 1
                        if ic == 11 :
                            del teamopponents [ 10 ]
                            ic -= 1
                    else:
                        result = re.search ( r'/ranking/teams' , str ( b ) )
                        if result != None :
                            result = re.search ( r'#' , str(b.text ) )
                            if result != None :
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
        # print(teamslink)
        #1
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
        #Получение времени
        timenow = time.strftime("%H:%M")
        s = requests.get( 'https://www.hltv.org' + str(con))
        soup = BS (s.content , 'html.parser')
        for q in soup.findAll('div', class_= 'timeAndEvent'):
            timer = q.select('.time')
            #print(timer[0].text)
            timer = timer[0].text
        #print(timer.replace(time.strftime("%H:"), ""))
        result = re.split(r':',timer,maxsplit=1)
        rusult = re.split(r':',timenow,maxsplit=1)
        #print(result,rusult)
        print ( str ( teamname [ 0 ] ) + "-" + str ( teamname [ 1 ] ) )
        connection = connect()
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
                        text = text + str(teamname[0])
                    else:
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


