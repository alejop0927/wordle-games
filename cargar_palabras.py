from app import app, db
from app import Word

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        word_count = Word.query.count()
        if word_count > 0:
            print(f'La base de datos contiene {word_count} palabras.')
        else:
            print('La base de datos está vacía.')

        # Abre el archivo de palabras
        with open('palabras.txt', 'r') as file:
            # Lee las líneas del archivo
            palabras = file.readlines()

        # Elimina espacios en blanco y saltos de línea de las palabras
        palabras = [palabra.strip() for palabra in palabras]

        # Agrega las palabras a la base de datos
        for palabra in palabras:
            nueva_palabra = Word(word=palabra)
            db.session.add(nueva_palabra)

        # Guarda los cambios en la base de datos
        db.session.commit()

        print('Palabras agregadas con éxito.')

