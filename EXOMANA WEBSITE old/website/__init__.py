from flask import Flask
# Unsere Datenbank
from flask_sqlalchemy import SQLAlchemy
# Aus dem Betriebsystem
from os import path
# managed alle einlogg Sachen
from flask_login import LoginManager

# Erstelle das Datenbank Objekt und gib ihm einen Namen
db = SQLAlchemy()
DB_NAME = "database.db"

# Erstelle die Flask Applikation, Quasi die Webseite


def create_app():
    # Die app wird mit der "Flask" funktion und dem Namen "__name__" initialisiert
    app = Flask(__name__)
    # Der Secret Key wird benutzt um Cookies und Session Data zu verschlüsseln
    app.config['SECRET_KEY'] = 'sogeheimuwu'
    # Sage Flask, wo die Datenbank gespeichert wird. Diese ist nun unter dem DB_Namen im Website Ordner
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Starte die Datenbank, wie beschrieben
    db.init_app(app)

    # Applikation wird gesagt, dass in .views ein Blueprint namens views exestieren
    from .views import views
    # selbes für auth
    from .auth import auth

    # Die importierten blueprints werden nun registriert und einem url_prefix zugeordnet
    # Wohin müsste ich gehen um zu allen URL in dem entsprechenden Blueprint zu gelangen
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/auth/') würde bedeuten, dass alle URL in auth.py vorangeschrieben /auth/ haben

    # damit der Code in der Models datei ausgeführt wird und die Klassen darin erstellt sind, bevor wir die Datenbank erstellen
    from .models import User, Note

    # Erstelle die Datenbank, wenn noch nicht vorhanden
    with app.app_context():
        db.create_all()
        print('Database created')

    # Erstelle die Datenbank - nicht benötigt
    # create_database(app)

    loginManager = LoginManager()
    # Wenn man sich einloggen muss um was zu sehen, wird man zur login Seite gebracht
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    # Sagt Flask, wie man einen Nutzer lädt, hier also indem man die id sucht
    @loginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Funktioniert nichtmehr in SQLAlchemy 3 und ist auch nicht benötigt. create_all() erstellt nun sowieso nur nich exestierende Datenbanken

# gucke ob wir schon eine Datenbank haben, wenn nicht erstellen wir eine
# def create_database(app):
    # Wenn die Datenbank nicht existiert
    # if not path.exists('website/' + DB_NAME):
    # Erstelle eine Datenbank. für die Aktuelle app
    # db.create_all(app=app)
    # print('Created Database')
