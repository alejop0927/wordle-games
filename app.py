#si puedes ver el Readme me seria de gran ayuda.

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///palabras_Wordle.db'
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)

@app.route('/jugar')
def inicio():
    palabra_aleatoria = random.choice(Word.query.all())
    return render_template('pagina/index.html', palabra=palabra_aleatoria.word)

@app.route('/probar', methods=['POST'])
def probar_conjetura():
    conjetura = request.form.get('conjetura')
    palabra_aleatoria = random.choice(Word.query.all())
    if conjetura == palabra_aleatoria.word:
        mensaje = "¡Adivinaste la palabra!"
    else:
        mensaje = "La conjetura es incorrecta. Inténtalo de nuevo."

    return render_template('pagina/index.html', palabra=palabra_aleatoria.word, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)
