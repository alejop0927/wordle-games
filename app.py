from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from werkzeug.middleware.shared_data import SharedDataMiddleware

app = Flask(__name__)

# Ruta para servir archivos estáticos desde la carpeta 'funcionalidad'
app.add_url_rule('/funcionalidad/<path:filename>', 'static', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/funcionalidad': './funcionalidad'})

app.secret_key = 'your_secret_key'  # Define una clave secreta para la sesión

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///palabras_Wordle.db'
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)

def word_to_dict(word):
    return {'id': word.id, 'word': word.word}

def dict_to_word(word_dict):
    return Word(id=word_dict['id'], word=word_dict['word'])

@app.route('/jugar', methods=['GET', 'POST'])
def jugar():
    if 'palabra_aleatoria' not in session:
        palabra_aleatoria = random.choice(Word.query.all())
        session['palabra_aleatoria'] = word_to_dict(palabra_aleatoria)

    palabra = dict_to_word(session['palabra_aleatoria'])
    mensaje = ''
    clases_css = []
    conjetura = []

    if request.method == 'POST':
        conjetura = request.form.getlist('conjetura[]')  # Ahora se obtiene como una lista
        conjetura = ''.join(conjetura)  # Convierte la lista en una cadena
        if conjetura == palabra.word:
            mensaje = "¡Adivinaste la palabra!"
            
    elif len(conjetura) == len(palabra.word):
        for i in range(len(conjetura)):
            if conjetura[i] == palabra.word[i]:
                clases_css.append('letra correcta')
            elif conjetura[i] in palabra.word:
                clases_css.append('letra casi correcta')
            else:
                clases_css.append('letra no perteneciente')
            
    else:
        mensaje = ""

    return render_template('pagina/index.html', palabra=palabra.word, mensaje=mensaje, clases_css=clases_css, conjetura=conjetura)

if __name__ == '__main__':
    app.run(debug=True)
