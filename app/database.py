import pymysql.cursors, time
from flask import jsonify
from datetime import datetime, timedelta

class MySQL:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def GetSettings(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from settings"
                cursor.execute(sql)
                result = cursor.fetchone()
                connection.commit()
            return result

    def GetBTCPayClient(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT btcPayClient from settings")
                result = cursor.fetchone()
                connection.commit()
            return result['btcPayClient']

    def SetBtcPayClient(self, btcPayClient):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE settings SET btcPayClient=%s"
                result = cursor.execute(sql, (btcPayClient))
                connection.commit()

    def GetLogin(self, email, password):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from users WHERE email=%s AND password=%s"
                cursor.execute(sql, (email, password))
                result = cursor.fetchone()
                connection.commit()
            return result

    def GetUserByEmail(self, email):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from users WHERE email=%s"
                cursor.execute(sql, (email))
                result = cursor.fetchone()
                connection.commit()
            return result

    def Insert(self, table, insert):
        keys = ', '.join([f"{k}" for k in insert.keys()])
        values = ', '.join([f"%s" for v in insert.values()])
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql= f"INSERT INTO {table} ({keys}) VALUES ({values})"
                valuesList = list(insert.values())
                cursor.execute(sql, tuple(valuesList))
                connection.commit()

    def UpdateSettings(self, settings):
        string = ', '.join([f"{i} = %s" for i in settings.keys()])
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql= f"UPDATE settings SET {string}"
                newList = list(settings.values())
                cursor.execute(sql, tuple(newList))
                connection.commit()
                print(cursor._last_executed)

    def GetAllTickets(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from tickets"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            return result

    def GetAllMembers(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from users"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            return result

    def GetAllInvoices(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from invoices"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            return result