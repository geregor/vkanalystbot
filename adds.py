import pymysql.cursors
from boto.s3.connection import S3Connection
import os

hostt = S3Connection(os.environ['HOST'])
usert = S3Connection(os.environ['USER'])
passwordt = S3Connection(os.environ['PASS'])

def connect():
    connection = pymysql.connect(
        host=hostt,
        user=usert,
        password=passwordt,
        db=usert,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

# Тир 1 - 1-7
# Тир 2 - 8-15
# Тир 3 - 16-25
# Тир 4 - 26 - ...
