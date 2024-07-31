from flask import Flask, jsonify, request
from helpers import funcoesApi

app = Flask(__name__)

# Rotas dos videos
@app.route('/')
def home():
    return jsonify({"aviso": "'API NO AR'"})

@app.route('/videos', methods=["GET"])
def videos():
    """ Listando os videos e informações """   
    categoria_titulo = request.args.get('search')
    if categoria_titulo:
        categoria_id = ''
        result = funcoesApi.videoCtgr(categoria_id, categoria_titulo)
        return jsonify(result)

    result = funcoesApi.listandoVideos()
    return jsonify(result)


@app.route('/addVideos', methods=['POST'])
def addVideos():
    """ Adicionando um novo vídeo """
    video_data = request.get_json()
    result = funcoesApi.adicionarVideo(video_data)
    return jsonify(result)

@app.route('/videos/<video_id>', methods=["GET", "DELETE", "PATCH", "PUT"])
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
    
    elif request.method == "PUT":
        video_data = request.get_json()
        if not video_data:
            return jsonify({"error": "Dados do vídeo não fornecidos"}), 400

        elif 'titulo' in video_data:
            campo = 'titulo'
            dados_campo = video_data[campo]
            result = funcoesApi.atualizarCampoVideo(video_id, campo, dados_campo)
            return jsonify(result)

        elif 'descricao' in video_data:
            campo = 'descricao'
            dados_campo = video_data[campo]
            result = funcoesApi.atualizarCampoVideo(video_id, campo, dados_campo)
            return jsonify(result)

        elif 'url' in video_data:
            campo = 'url'
            dados_campo = video_data[campo]
            result = funcoesApi.atualizarCampoVideo(video_id, campo, dados_campo)
            return jsonify(result)

        elif 'categoria' in video_data:
            campo = 'categoria'
            dados_campo = video_data[campo]
            result = funcoesApi.atualizarCampo(video_id, campo, dados_campo)
            return jsonify(result)

        else:
            return jsonify({"error": "Campo não encontrado nos dados enviados"})


# Rotas das Categorias
@app.route('/categorias', methods=['GET'])
def categorias():
    """ Listando categorias """
    result = funcoesApi.listandoCategorias()
    return jsonify(result)

@app.route('/categorias/<categoria_id>/videos/')
def listarVideosCtgr(categoria_id):
    categoria_titulo = ''
    result = funcoesApi.videoCtgr(categoria_id, categoria_titulo)
    return result

@app.route('/addCategorias', methods=['POST'])
def addCategorias():
    """ Adicionando um novo vídeo """
    categoria_data = request.get_json()
    result = funcoesApi.adicionarCategoria(categoria_data)
    return jsonify(result)

@app.route('/categorias/<categoria_id>', methods=["GET", "DELETE", "PATCH", "PUT"])
def getCategorias(categoria_id):
    if request.method == "GET":
        result = funcoesApi.selecionarCategoria(categoria_id)
        return jsonify(result)

    elif request.method == "DELETE":
        result = funcoesApi.deletarCategoria(categoria_id)
        return jsonify(result)

    elif request.method == "PATCH":
        categoria_data = request.get_json()
        result = funcoesApi.autalizarCategoria(categoria_id, categoria_data)
        return jsonify(result)

    elif request.method == "PUT":
        categoria_data = request.get_json()
        if not categoria_data:
            return jsonify({"error": "Dados do vídeo não fornecidos"}), 400

        elif 'titulo' in categoria_data:
            campo = 'titulo'
            dados_campo = categoria_data[campo]
            result = funcoesApi.atualizarCampoCategoria(categoria_id, campo, dados_campo)
            return jsonify(result)

        elif 'cor' in categoria_data:
            campo = 'cor'
            dados_campo = categoria_data[campo]
            result = funcoesApi.atualizarCampoCategoria(categoria_id, campo, dados_campo)
            return jsonify(result)

        else:
            return jsonify({"error": "Campo não encontrado nos dados enviados"})

if __name__ == '__main__':
    app.run(debug=True)