from flask import Flask, request, jsonify
#from flask_cors import CORS

from busquedas_no_informadas.Profundidad import dfs_izquierda_derecha
from busquedas_no_informadas.Amplitud import bfs

app = Flask(__name__)

#CORS(app)

#@app.route('/')
#def index():
#    return  app.send_static_file('index.html')



@app.route('/algorithms', methods=['POST'])
def run_algorithm():
    data = request.json
    inicio = data['Inicio']
    meta = data['Meta']
    mapa = data['Mapa']
    algoritmo = data['Algoritmo']

    
    if algoritmo == 'limitada_profundidad':
        dfs_izquierda_derecha(mapa, inicio, meta)
        loadImagen = True

    else:
        return jsonify({'error': 'Algoritmo no válido'}), 400 
    return jsonify({'confirmacion': loadImagen})
   




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)