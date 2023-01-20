# Hier werden die Datenbank modelle erstellt
# Wir wollen ein Model für die UserAccounts und eins für die Notizen erstellen

#import from . bedeutet "von diesem Paket also init file"
from . import db
# Gibt dem Benutzer ein paar eigene Attribute
from flask_login import UserMixin
# Um die Aktuelle Zeit auszulesen
from sqlalchemy.sql import func

# Modell für unsere Notizen
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Notiz darf 10000 Zeichen lang sein 
    data = db.Column(db.String(10000))
    # Speichert die Zeit des Erstellens der Notiz, sowie die Zeitzone
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Erstelle einen ForeignKey (Referenz auf andere Datenbank). Hier: wer hat die Notiz erstellt. db.ForeignKey stellt sicher, dass die id valide ist.
    # In 'user.id' steht user für die Tabelle(lower case in sql) und id für die entsprechende Spalte.
    # ForeignKey ist nur manytoOne Beziehungen
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


# Erstelle das Modell "User" ist der Name (singular) erbt von db.Model und UserMixin
class User(db.Model, UserMixin):
    # Einzigartige Zuordnungsnummer als Integer (genannt primary_key)
    id = db.Column(db.Integer, primary_key=True)
    # zugeordnete email mit maximal 150 Zeichen und darf nur einmal in der Datenbank sein (unique)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # Alle Notizen, die ein Benutzer erstellt hat sollen hier auch zugreifbar sein (Upper case braucht man hier.)
    notes = db.relationship('Note')
