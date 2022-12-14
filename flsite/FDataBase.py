import math , time
import sqlite3


class FDateBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Ошибка чтения БД')

        return []

    def addPost(self,title,text,url):
        try:

            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()# fetchone() позволяет вызвать следующую строку из набора результатов запроса, показывая только одну запись,fetchAll() позволяет извлечь все (оставшиеся) строки результата запроса, возвращая их в виде последовательности последовательностей.
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False

            tm= math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?,?,?,?)",(title,text,url,tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД'+ str(e))
            return False
        return True

    def getPost(self,alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из DB '+ str(e))

        return (False,False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из DB ' + str(e))
        return []