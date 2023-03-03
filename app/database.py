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

    def GetAllMembers(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from users"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            return result

    def SaveUserSettings(self, userId, data):
        string = ', '.join([f"{i} = %s" for i in data.keys()])
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql= f"UPDATE users SET {string} WHERE id=%s"
                newList = list(data.values())
                newList.append(userId)
                cursor.execute(sql, tuple(newList))
                connection.commit()

    def GetProviders(self):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from providers"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
            return result

    def GetRecoveryInfo(self, email, code):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from recovery WHERE email=%s AND code=%s"
                cursor.execute(sql, (email, code))
                result = cursor.fetchone()
                connection.commit()
            return result

    def MarkRecovered(self, email, code):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE recovery SET recovered = %s WHERE email=%s AND code=%s"
                cursor.execute(sql, (1, email, code))
                connection.commit()

    def GetServices(self, providerId):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from services WHERE provider=%s"
                cursor.execute(sql, (providerId))
                result = cursor.fetchall()
                connection.commit()
            return result

    def GetServiceById(self, serviceId):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from services WHERE id=%s"
                cursor.execute(sql, (serviceId))
                result = cursor.fetchone()
                connection.commit()
            return result

    def GetTicketsById(self, userId):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from tickets WHERE ownerId=%s"
                cursor.execute(sql, (userId))
                result = cursor.fetchall()
                connection.commit()
            return result

    def GetTemplates(self, username):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from templates WHERE ownerId=%s"
                cursor.execute(sql, (username))
                result = cursor.fetchall()
                connection.commit()
            return result

    def DeleteTemplateById(self, id):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM templates WHERE id=%s"
                cursor.execute(sql, (id))
                connection.commit()

    def GetTemplateById(self, templateId):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from templates WHERE id=%s"
                cursor.execute(sql, (templateId))
                result = cursor.fetchone()
                connection.commit()
            return result

    def GetActiveTicketsById(self, userId):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from tickets WHERE ownerId=%s AND complete=%s"
                cursor.execute(sql, (userId, False))
                result = cursor.fetchall()
                connection.commit()
            return result

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

    def GetOrdersByOwnerId(self, ownerId):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * from orders WHERE ownerId=%s"
                cursor.execute(sql, (ownerId))
                result = cursor.fetchall()
                connection.commit()
            return result

    def AddBalanceToUser(self, email, amount):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET balance = balance + %s WHERE email=%s"
                cursor.execute(sql, (amount, email))
                connection.commit()

    def UpdateUserPassword(self, email, password):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET password = %s WHERE email=%s"
                cursor.execute(sql, (password, email))
                connection.commit()

    def RemoveBalanceFromUser(self, email, amount):
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET balance = balance - %s WHERE email=%s"
                cursor.execute(sql, (amount, email))
                connection.commit()

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

    def UpdateTicket(self, ticketId, data):
        string = ', '.join([f"{i} = %s" for i in data.keys()])
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql= f"UPDATE tickets SET {string} WHERE id=%s"
                newList = list(data.values())
                newList.append(ticketId)
                cursor.execute(sql, tuple(newList))
                connection.commit()
                print(cursor._last_executed)

    def UpdateTemplate(self, templateId, data):
        string = ', '.join([f"{i} = %s" for i in data.keys()])
        connection = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database, cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql= f"UPDATE templates SET {string} WHERE id=%s"
                newList = list(data.values())
                newList.append(templateId)
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