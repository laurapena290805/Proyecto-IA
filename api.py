from flask import Flask, request, jsonify
from flask_cors import CORS
from Busquedas import ejecutar_busquedas

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "API Activada"

@app.route('/algorithms', methods=['POST'])
def run_algorithm():
    data = request.json
    mapa = data['Mapa']
    meta = data['Meta']
    inicio = data['Inicio']
    maximo_iteraciones = data['MaximoIteraciones']

    check = ejecutar_busquedas(mapa, meta, inicio, maximo_iteraciones)

    return jsonify(check)

if __name__ == '__main__':
    app.run(debug=True)