# Hier stehen alle Pfade, die mit einer anmeldung verbunden sind
# request muss importiert werden um Infos vom Html erhalten zu können
# flash erlaubt kurze popup feedbacknachrichten auf der Webseite anzuzeigen
from flask import Blueprint, render_template, request, flash, redirect, url_for
# importiere das User Element der Datenbank
from .models import User
from . import db
# Um Passwort Hashing zu betreiben
from werkzeug.security import generate_password_hash, check_password_hash
# Lass den Nutzer verschiedene Login/Logout rollen annehmen
from flask_login import login_user, login_required, logout_user, current_user


# wie in views.py
auth = Blueprint('auth', __name__)

# Damit unser Back End POST requests empfangen kann, muss es hier spezifiziert werden. Sonst können wir nur GET requests empfangen


@auth.route('/login', methods=['GET', 'POST'])
def login():

    # Man kann an Jinja Variablen senden, mit der render_template funktion. Das Template erhält hier die Variable "boolean" = False
    # return render_template("login.html", boolean = False)
    # Mehrere Variablen gehen auch

    # request enthält alle möglichen Informationen, die von der Webseite übermittelt werden(z.b. URL)
    # mit request.form erhalten wir alle Informationen in dem "form" in html
    # Problem ist, dass dies ausgeführt wird unabhängig von GET und POST request und deshalb die Daten immer üüberschrieben werden (mit nichts)
    # data = request.form
    # print(data)

    # Login

    # beim Abschicken definiere die eingegebenen Daten
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Überprüfe die Daten
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # login den aktuellen Nutzer und lasse ihn eingeloggt solange die Session läuft
                login_user(user, remember=True)

                # Bringe den eingelogten Nutzer zur Home Page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Nach dem logout wird zum login screen redirected
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if Bedingungen um zwischen den methoden GET und POST zu unterscheiden.
    if request.method == 'POST':
        # Setze die Variablen gleich der im form abgefragten eingaben mithilfe der get funktion
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Checke ob die Email schon existiert
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        # simple Überprüfungen ob die Eingaben stimmen können
        elif len(email) < 4:
            # Die Flash methode zeigt eine Popup Nachricht auf der Webseite an.
            # Die category können wir benutzen um allen Nachrichten des entsprechenden typs gewisse Attribute, wie Farbe zu geben
            flash('Email must be greater than 3 chraraters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 chraraters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 chraraters.', category='error')
        else:
            # add new user to database
            # Das Passwort wird als Hash gespeichert
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method="sha256"))
            # Füge Benutzer der Datenbank hinzu
            db.session.add(new_user)
            db.session.commit()
            # login user after sign up
            login_user(new_user, remember=True)
            # zeige Nachricht
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
