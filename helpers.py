import sqlite3
import requests

class funcoesApi():
    def listandoVideos():
        """ Listando os videos e informações """

        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("SELECT * FROM banco_video")
        rows = cur.fetchall()
        
        column_names = [description[0] for description in cur.description]
        result = [dict(zip(column_names, row)) for row in rows]

        con.close()
        return result
    
    def selecionarVideo(video_id):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM banco_video WHERE ID = {video_id}")
        rows = cur.fetchall()

        if rows:
            column_names = [description[0] for description in cur.description]
            result = [dict(zip(column_names, row)) for row in rows]
            con.close()
            return result
        
        result = {
            'alerta': 'Vídeo não encontrado!'
        }
        return result
    
    def adicionarVideo(video_data):
        if not isinstance(video_data, dict):
            return {'erro': 'Dados inválidos. Esperado um dicionário JSON.'}
        try:
            titulo = video_data['titulo']
            descricao = video_data['descricao']
            url = video_data['url']
        except KeyError as e:
            return {'alerta': f'Campo ausente: {e.args[0]}'}

        if requests.get(url).status_code == 400:
            return {'alerta': 'URL indisponível'}
        
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("INSERT INTO banco_video (titulo, descricao, url) VALUES (?, ?, ?)", (titulo, descricao, url))
        con.commit()
        video_id = cur.lastrowid
        con.close()

        result = {
            'ID': video_id,
            'titulo': video_data['titulo'],
            'descricao': video_data['descricao'],
            'Url': video_data['url']
        }
        return result

    def deletarVideo(video_id):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        try:
            cur.execute(f"DELETE FROM banco_video WHERE id={video_id}")
            con.commit()
            result = {'alerta': 'Video deletado com sucesso!'}
            return result
        except Exception as error:
            error = str(error)
            result = {'alerta': f'{error}'}
            return result

    def autalizarVideo(video_id, video_data):
        if not isinstance(video_data, dict):
            return {'erro': 'Dados inválidos. Esperado um dicionário JSON.'}
        try:
            titulo = video_data['titulo']
            descricao = video_data['descricao']
            url = video_data['url']
        except KeyError as e:
            return {'alerta': f'Campo ausente: {e.args[0]}'}

        if not titulo or not titulo.strip():
            return {'alerta': 'O campo "titulo" deve ser preenchido.'}
        if not descricao or not descricao.strip():
            return {'alerta': 'O campo "descricao" deve ser preenchido.'}
        if not url or not url.strip():
            return {'alerta': 'O campo "url" deve ser preenchido.'}

        if requests.get(url).status_code == 400:
            return {'alerta': 'URL indisponível'}
        
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("UPDATE banco_video SET titulo=?, descricao=?, url=? WHERE id=?", (titulo, descricao, url, video_id))
        con.commit()

        cur.execute(f"SELECT * FROM banco_video WHERE ID = {video_id}")
        rows = cur.fetchall()

        if rows:
            column_names = [description[0] for description in cur.description]
            result = [dict(zip(column_names, row)) for row in rows]
            con.close()
            return result
    
