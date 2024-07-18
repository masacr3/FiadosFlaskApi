from tinydb import TinyDB, Query

def init_db():
    #path = './mysite/db.json'
    path = './db.json'
    db = TinyDB(path)
    User = Query()

    #inicializo las tablas
    checkPagos = db.get(User.pagos.exists())
    checkUsuarios = db.get(User.usuarios.exists())
    
    if not checkPagos:
        db.insert({'pagos' : []})
    
    if not checkUsuarios:
        db.insert({"usuarios" : []})
    
    return db, User