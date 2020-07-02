import pymysql.cursors

#Username: VcJhVl8VY9
#Database name: VcJhVl8VY9
#Password: 2szV2WF4BO
#Server: remotemysql.com
#Port: 3306
#These are the username and password to log in to your database and phpMyAdmin

def connect():
    connection = pymysql.connect(
        host='remotemysql.com',
        user='VcJhVl8VY9',
        password='2szV2WF4BO',
        db='VcJhVl8VY9',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

# Тир 1 - 1-7
# Тир 2 - 8-15
# Тир 3 - 16-25
# Тир 4 - 26 - ...
