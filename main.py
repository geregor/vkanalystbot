import requests
from bs4 import BeautifulSoup as BS
import re
from time import sleep
import time
import vk_api
import vk
#Узнаем будущие матчи и сейчашние
token = '8f8b935dbc09eab696c9e1b710c8bd99bbd6be6460f4177efcedac4af43f237908f17329e983683a168b8'

vk = vk_api.VkApi("+375336671825", "KoLeRiNo")
vk.auth()
while True:


    r = requests.get('https://www.hltv.org/matches')
    soup = BS(r.content, 'html.parser')
    teams = []
    for link in soup.findAll('a'):
        result = re.search(r'/matches/', str(link))
        if result != None:
            teams.append(link.get('href'))
    #print(teams)
    qer = list(range(10))
    i = 0
    timeforsleep = 0
    #Узнаем проценты на команду
    for i in teams:
        con = i
        timeforsleep += 1
        s = requests.get ( 'https://www.hltv.org' + str ( con ) )
        soup = BS ( s.content , 'html.parser' )
        teampercent = []
        for q in soup.findAll('div', class_='percentage'):
            teampercent.append(q.text)
        team = []
        for q in teampercent:
            lol = q
            team.append(float(lol.replace ( "%" , "" )))
        teampercent = team
        #Получение названия команды
        s = requests.get ( 'https://www.hltv.org' + str ( con ) )
        soup = BS ( s.content , 'html.parser' )
        teamname = []
        for q in soup.findAll('div', class_='teamName'):
            teamname.append(q.text)
        #print(str(teamname))
        #Получение времени
        timenow = time.strftime("%H:%M")
        s = requests.get( 'https://www.hltv.org' + str ( con ) )
        soup = BS ( s.content , 'html.parser' )
        for q in soup.findAll('div', class_= 'timeAndEvent'):
            timer = q.select('.time')
            print(timer[0].text)
            timer = timer[0].text
        #print(timer.replace(time.strftime("%H:"), ""))
        result = re.split(r':',timer,maxsplit=1)
        rusult = re.split(r':',timenow,maxsplit=1)
        #print(result,rusult)
        text = ""
        if teampercent[1]-teampercent[0] > 0:
            text = text + str(teamname[1])
        else:
            text = text + str(teamname[0])
        if int(result[0]) == (int(rusult[0])+3):
                print("[БОТ]Приближается матч между "+teamname[0]+" и "+teamname[1]+"\nШансы: "+str(teampercent[0])+" на "+str(teampercent[1])+"\nОчень ожидаемо что выйграют "+text)
                vk.method("wall.post", {"from_group": 1, "owner_id": -154885097, "message": "[БОТ]Приближается матч между "+teamname[0]+" и "+teamname[1]+"\nШансы: "+str(teampercent[0])+" на "+str(teampercent[1])+"\nОчень ожидаемо что выйграют "+text})

    #Классно
        if timeforsleep == 10:
            timeforsleep = 0
            print("Отдыхаем")
            sleep(3600)


