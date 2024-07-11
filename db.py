from tinydb import TinyDB, Query

def init_db():
    #path = './mysite/db.json'
    path = './db.json'
    db = TinyDB(path)
    User = Query()
    return db, User