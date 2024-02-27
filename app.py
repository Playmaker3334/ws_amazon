from flask import Flask, request, jsonify
from Ws_Amazon import *
app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return "Bienvenido al servidor de prueba!"

@app.route('/scrap', methods=['POST'])
def scrap():
    data = request.json
    r = Scrapper(data["url"]).scrape_sync()
    return jsonify({'message': 'Datos recibidos con éxito!', 'result': r})

@app.route('/status', methods=['GET'])
def server_status():
    return jsonify({'status': 'Activo'})

if __name__ == '__main__':
    app.run(port=6000,debug=True)
