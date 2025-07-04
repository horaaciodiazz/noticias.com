from flask import Flask, render_template, request
from noticias import buscar_noticias   # función que devuelve string o lista

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    resultado = None
    if request.method == 'POST':
        q = request.form.get('query')
        resultado = buscar_noticias(q)
        print(resultado)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
