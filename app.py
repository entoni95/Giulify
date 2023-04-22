from flask import Flask, render_template, redirect, request, session
from werkzeug.utils import secure_filename
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash


import podcast_dao

app = Flask(__name__)
#per attivare la sessione su server
#app.secret_key = "chiave segreta"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False #altrimenti la sessione rimane attiva per sempre
Session(app)

@app.route("/")
def index():
    podcast = podcast_dao.get_podcast()
    return render_template('index.html', podcast=podcast)

@app.route("/subscribe")
def subscribe():
    return render_template('subscribe.html')

@app.route("/podcast/<int:id>")
def single_podcast(id):
    id_podcast = id
    my_podcast = podcast_dao.get_single(id_podcast)
    comments = podcast_dao.get_comments(id_podcast)
    return render_template('single.html', id_podcast=id, my_podcast=my_podcast, comments=comments)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        #salvo i valori inviati dall'utente
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        ruolo = request.form.get("ruolo")
        rows = podcast_dao.login(nickname, ruolo)
        #possono verificarsi due casi: o rows è vuoto perché l'utente non esiste oppure non appartiene a quel ruolo
        #oppure l'utente esiste ed appartiene a quel ruolo, ma la password non è corretta
        if rows:
            for row in rows:
                if check_password_hash(row["password"], password):
                    session["id"] = row["id"]
                    session["name"] = nickname
                    session["ruolo"] = ruolo
                else:
                    session["id"] = -1
        else:
            session["id"] = -1
    return redirect('/')

@app.route("/new-comment", methods=['POST', 'GET'])
def new_comment():
    if request.method == "POST":
        id_utente = request.form.get("id_utente")
        id_podcast = request.form.get("id_podcast")
        testo = request.form.get("testo")
        podcast_dao.add_comment(id_podcast, id_utente, testo)
        my_podcast = podcast_dao.get_single(id_podcast)
        comments = podcast_dao.get_comments(id_podcast)
    return render_template('single.html', my_podcast=my_podcast, comments=comments)

@app.route("/delete_comment/<int:id>")
def delete_comment(id):
    id_comment = id
    podcast_dao.delete_comment(id_comment)
    return redirect('/')

@app.route("/delete_episode/<int:id>")
def delete_episode(id):
    id_episode = id
    podcast_dao.delete_episode(id_episode)
    return redirect('/')

@app.route("/new-podcast", methods=['POST', 'GET'])
def new_podcast():
    if request.method == "POST":
        id_creatore = request.form.get("id_utente")

        nome_podcast = request.form.get("nome_podcast")

        if request.files["img_podcast"]:
            uploaded_file = request.files["img_podcast"]
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(f'static/{filename}')
        else:
            filename = "default.jpg"

        descrizione = request.form.get("content")

        categoria = request.form.get("categoria")

        podcast_dao.new_podcast(id_creatore, nome_podcast, descrizione, categoria, filename)

    return redirect('/')

@app.route("/new-episode", methods=['POST', 'GET'])
def new_episode():
    if request.method == "POST":
        id_podcast = request.form.get("id_podcast")

        nome_episodio = request.form.get("nome_episodio")

        if request.files["file_audio"]:
            uploaded_file = request.files["file_audio"]
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(f'static/{filename}')
        else:
            filename = "default.mp3"

        descrizione = request.form.get("content")

        data_episodio = request.form.get("data_episodio")

        podcast_dao.new_episode(id_podcast, nome_episodio, descrizione, data_episodio, filename)

    return redirect('/')

@app.route("/new-user", methods=['POST', 'GET'])
def new_user():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        password = generate_password_hash(password, method='sha256')
        ruolo = request.form.get("ruolo")
        rows = podcast_dao.new_user(nickname, password, ruolo)
        if rows:
            for row in rows:
                session["id"] = row["id"]
            session["name"] = nickname
            session["ruolo"] = ruolo
        else:
            session["id"] = -2
    return redirect('/')

@app.route("/logout")
def logout():
    session["id"] = ""
    session["name"] = ""
    session["ruolo"] = ""
    return redirect('/')