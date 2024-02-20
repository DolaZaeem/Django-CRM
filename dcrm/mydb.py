import mysql.connector
dataBase = mysql.connector.connect(
    host= 'localhost',
    user = 'root',
    passwd = '12345'
)

#cursor
cursorObject = dataBase.cursor()

#create db

cursorObject.execute('CREATE DATABASE elderco')

print('done')