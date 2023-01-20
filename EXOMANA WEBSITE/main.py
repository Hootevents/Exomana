# Immer wenn man in einen Ordner die "__init__.py" datei packt, wird sie zu einem Python Paket
# Aus dem Paket (der "__init__.py" Datei ) können nun funktionen importiert werden
from website import create_app

app = create_app()

# Die Webeite wird nur gestartet, wenn man "main.py" direkt startet und nicht wenn es importiert ist
# Sonst wäre der __name__ anders
if __name__ == '__main__':
    # starte die Flask applikation
    app.run(debug=True)
    # debug = True heißt, dass bei jeder Änderung die Applikation neu gestartet wird
    
