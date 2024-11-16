from flask import Flask, request, jsonify
from flask_cors import CORS
from main import ejecutar_busquedas

app = Flask(__name__, static_folder='web', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/algorithms', methods=['POST'])
def run_algorithm():
    data = request.json
    inicio = data['Inicio']
    meta = data['Meta']
    mapa = data['Mapa']
    maximo_iteraciones = data['MaximoIteraciones']

    resultados = ejecutar_busquedas(mapa, meta, inicio, maximo_iteraciones)
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)