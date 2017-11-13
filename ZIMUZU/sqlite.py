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
        conn.row_factory = dic_factory
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
    cursor.execute("SELECT name,season,episode FROM drama;")
    return cursor.fetchall()


@getCursor
def updateData(cursor, name, season, episode):
    cursor.execute("UPDATE drama SET season={0}, episode ={1} WHERE name='{2}'".format(season, episode, name))


def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == '__main__':
    updateData('南方公园', 21, 5)
    value = getAll()
    print(value)
