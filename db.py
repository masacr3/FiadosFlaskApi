from tinydb import TinyDB, Query

def init_db():
    #path = './mysite/db.json'
    path = './db.json'
    db = TinyDB(path)
    User = Query()
    checkPagos = db.get(User.pagos.exists())
    print(f'estoy en init', checkPagos)
    if not checkPagos:
        db.insert({'pagos' : []})
    return db, User