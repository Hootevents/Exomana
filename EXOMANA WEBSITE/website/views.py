# Hier kommen die Pfade rein, zu denen ein Nutzer navigieren kann, die nichts mit anmeldung zu tun haben
# Mit der render_tempplate function werden die html templates zu einer webseite geformt
from flask import Blueprint, render_template, request, flash, jsonify
from . import db
from .models import Note, Character
import json

from flask_login import login_required, current_user
# Wir erstellen einen Blueprint, damit wir hier unsere URLs definieren können und den tatsächlichen Inhalt von anderen Dateien beziehen können
views = Blueprint('views', __name__)

# Der Pfad eines Blueprints wird so definiert:


@views.route('/', methods=['GET', 'POST'])
# wird nur eingeloggten Nutzern gezeigt
@login_required
# Wann immer zu der URL navigiert wird, wird die home funktion ausgeführt
def home():
    # Hier könnte man nun einfach html zurückgeben
    # return "<h1>Test</h1>" - Auf der Webseite steht "Test"

    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) <= 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    # In die render_template funktion tragen wir nun einfach den Namen des zu rendernden Templates ein.
    return render_template("home.html", user=current_user)


@views.route('/characters', methods=['GET', 'POST'])
@login_required
def characters():
    if request.method == 'POST':
        # add character to Database
        character_name = request.form.get('character_name')
        # Achtung! Character Splitter ist ein String hier, da die request funktion immer einen string returned
        character_splitter = request.form.get('character_splitter')
        if len(character_name) <= 1:
            flash('Bitte gib dem Charakter einen Namen')
        elif len(character_splitter) < 1:
            flash('Bitte trag ein, wie viele Splitter der Charakter besitzt')
        else:
            character_splitter = int(character_splitter)
            new_character = Character(
                name=character_name, splitter=character_splitter, user_id=current_user.id)
            db.session.add(new_character)
            db.session.commit()
            flash('Charakter hinzugefügt', category='success')

    return render_template("characters.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
