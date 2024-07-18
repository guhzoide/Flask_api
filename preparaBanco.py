import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

def preparaBanco():
    cur.execute("""
                CREATE TABLE videos(
                    ID int IDENTITY(1,1) NOT NULL, 
                    titulo varchar(30), 
                    descricao varchar(60), 
                    url varchar(100)
                )
    """)

def inserirBanco():
    cur.execute("""
        INSERT INTO banco_video (titulo, descricao, url)
        VALUES ('teste', 'teste', 'teste')
    """)
    con.commit()

def deletarVideo():
    cur.execute("""
        delete from banco_video
    """)
    con.commit()

deletarVideo()