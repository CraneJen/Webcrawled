import sqlite3


def createDB():
    conn = sqlite3.connect('zimuzu.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS drama
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        season INT NOT NULL,
        episode INT NOT NULL
        );
        ''')
    cursor.close()
    conn.commit()
    conn.close()


def getCursor(func):
    def __call(*args, **kwargs):
        conn = sqlite3.connect('zimuzu.sqlite3')
        cursor = conn.cursor()
        action = func(cursor, *args, **kwargs)

        conn.commit()
        cursor.close()
        conn.close()
        return action
    return __call


@getCursor
def insertData(cursor, name, season, episode):
    cursor.execute("INSERT INTO drama (name,season,episode) \
   VALUES ('{0}',{1},{2});".format(name, season, episode))
    print(cursor.rowcount)


@getCursor
def getByName(cursor, name):
    cursor.execute("SELECT * FROM drama WHERE name='{0}';".format(name))
    value = cursor.fetchall()
    return value


@getCursor
def getAll(cursor):
    cursor.execute("SELECT * FROM drama;")
    return cursor.fetchall()


@getCursor
def updateData(cursor, name, season, episode):
    cursor.execute("UPDATE drama SET season={0}, episode ={1} WHERE name='{2}'".format(season, episode, name))


if __name__ == '__main__':
    value = getAll()
    print(value)

    # try:
    #     updateData('硅谷', 11, 2)
    # except Exception as e:
    #     # raise e
    #     print(e)
    # else:
    #     insertData('硅谷', 11, 2)
    # finally:
    #     datas = getAll()

    # for data in datas:
    #     print('name: {}'.format(data[1]))
    #     print('season: {}'.format(data[2]))
    #     print('episode: {}'.format(data[3]))
    #     print('\n')
