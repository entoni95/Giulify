import sqlite3

def get_podcast():
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row #non una stringa ma un dizionario di parole
    sql = "SELECT utenti.nickname, podcast.id, podcast.titolo, podcast.descrizione, podcast.categoria, podcast.immagine " \
          "FROM podcast " \
          "INNER JOIN utenti " \
          "ON podcast.id_creatore=utenti.id"
    cursor = conn.cursor()
    cursor.execute(sql)
    podcast = cursor.fetchall()
    cursor.close()
    conn.close()
    return podcast

def get_single(id):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "SELECT podcast.id AS id_podcast, podcast.titolo, podcast.descrizione, podcast.categoria, podcast.immagine, podcast.id_creatore, " \
          "episodi.id AS id_episodio, episodi.file_audio, episodi.titolo_episodio, episodi.descr_episodio, episodi.data " \
          "FROM episodi " \
          "INNER JOIN podcast " \
          "ON episodi.id_podcast=podcast.id " \
          "WHERE episodi.id_podcast = ? " \
          "ORDER BY episodi.data ASC"
    cursor = conn.cursor()
    cursor.execute(sql, (id, ))
    podcast = cursor.fetchall()
    cursor.close()
    conn.close()
    return podcast

def get_comments(id):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "SELECT utenti.nickname, commenti.id_utente, commenti.id AS id_commento, commenti.data_pubblicazione, commenti.testo " \
          "FROM commenti " \
          "INNER JOIN utenti " \
          "ON commenti.id_utente=utenti.id " \
          "WHERE commenti.id_podcast = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (id, ))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments

def login(nickname, ruolo):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "SELECT id, password FROM utenti WHERE nickname = ? AND ruolo = ?"
    cursor = conn.cursor()
    #restituirà solo un valore poiché il nickname è univoco oppure niente se non esiste l'utente oppure non appartiene
    #a quel determinato ruolo
    cursor.execute(sql, (nickname, ruolo, ))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def add_comment(id_podcast, id_utente, testo):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "INSERT INTO commenti (data_pubblicazione, testo, id_podcast, id_utente) " \
          "VALUES (CURRENT_DATE, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (testo, id_podcast, id_utente))
    conn.commit()
    cursor.close()
    conn.close()
    return ""

def new_podcast(id_creatore, titolo, descrizione, categoria, immagine):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "INSERT INTO podcast (titolo, descrizione, categoria, immagine, id_creatore) " \
          "VALUES (?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (titolo, descrizione, categoria, immagine, id_creatore))
    conn.commit()
    cursor.close()
    conn.close()
    return ""

def new_episode(id_podcast, nome_episodio, descrizione, data_episodio, filename):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "INSERT INTO episodi (file_audio, titolo_episodio, descr_episodio, data, id_podcast) " \
          "VALUES (?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(sql, (filename, nome_episodio, descrizione, data_episodio, id_podcast))
    conn.commit()
    cursor.close()
    conn.close()
    return ""

def delete_comment(id_commento):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "DELETE FROM commenti WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (id_commento, ))
    conn.commit()
    cursor.close()
    conn.close()
    return ""

def delete_episode(id_episodio):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "DELETE FROM episodi WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (id_episodio, ))
    conn.commit()
    cursor.close()
    conn.close()
    return ""

def new_user(nickname, password, ruolo):
    conn = sqlite3.connect('podcast_db.db')
    conn.row_factory = sqlite3.Row
    sql = "INSERT INTO utenti (nickname, password, ruolo) " \
          "VALUES (?, ?, ?)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nickname, password, ruolo))
        conn.commit()
        cursor.close()
    except:
        print('eccezione: la query è andata male oppure si è cercato di inserire un nickname già presente')

    #Ho creato l'utente (oppure no se il nickname è già presente). Effettuo adesso il login
    sql = "SELECT id FROM utenti WHERE nickname = ? AND password = ? AND ruolo = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (nickname, password, ruolo, ))
    id_user = cursor.fetchall()
    cursor.close()
    conn.close()
    return id_user
