from flask import Flask, jsonify, request
from helpers import funcoesApi

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"aviso": "'API NO AR'"})

@app.route('/videos')
def videos():
    """ Listando os videos e informações """
    result = funcoesApi.listandoVideos()
    return jsonify(result)

@app.route('/videos/<video_id>', methods=["GET", "DELETE", "PATCH"])
def getVideo(video_id):
    """ Selecionando/Deletar um video específico """
    if request.method == "GET":
        result = funcoesApi.selecionarVideo(video_id)
        return jsonify(result)
    
    elif request.method == "DELETE":
        result = funcoesApi.deletarVideo(video_id)
        return jsonify(result)

    elif request.method == "PATCH":
        video_data = request.get_json()
        result = funcoesApi.autalizarVideo(video_id, video_data)
        return jsonify(result)

@app.route('/addVideo', methods=['POST'])
def addVideo():
    """ Adicionando um novo vídeo """
    video_data = request.get_json()
    result = funcoesApi.adicionarVideo(video_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)