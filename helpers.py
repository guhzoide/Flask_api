import sqlite3
import requests

class funcoesApi():
    # Funcoes para videos
    def listandoVideos():
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("SELECT * FROM banco_videos")
        videos = cur.fetchall()

        result = []

        if videos:
            for video in videos:
                cur.execute("SELECT cor FROM banco_categoria WHERE titulo=?", (video[4],))
                cor = cur.fetchone()
                
                video_data = {
                    "id": video[0],
                    "titulo": video[1],
                    "descricao": video[2],
                    "categoria": video[4],
                    "cor": cor[0] if cor else None,
                    "url": video[3]
                }

                result.append(video_data)

        else:
            result = {
                'alerta': 'Video não encontrado!'
            }

        con.close()        
        return result

    def selecionarVideo(video_id):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM banco_videos WHERE ID = ?", (video_id,))
        videos = cur.fetchall()

        if videos:
            for video in videos:
                cur.execute("SELECT cor FROM banco_categoria WHERE titulo=?", (video[4],))
                cor = cur.fetchone()
                
                result = {
                    "id": video[0],
                    "titulo": video[1],
                    "descricao": video[2],
                    "categoria": video[4],
                    "cor": cor[0] if cor else None,
                    "url": video[3]
                }
        else:
            result = {
                'alerta': 'Video não encontrado!'
            }

        con.close()
        return result
    
    
    def adicionarVideo(video_data):
        if not isinstance(video_data, dict):
            return {'erro': 'Dados inválidos. Esperado um dicionário JSON.'}
        try:
            titulo = str(video_data['titulo'])
            descricao = str(video_data['descricao'])
            url = str(video_data['url'])

        except KeyError as e:
            return {'alerta': f'Campo ausente: {e.args[0]}'}
        
        if not titulo.strip() or not descricao or not descricao.strip() or not url or not url.strip():
            return {'alerta': 'Os campos devem ser preenchidos corretamente.'}

        elif requests.get(url).status_code == 400:
            return {'alerta': 'URL indisponível'}

        try:
            categoria = str(video_data['categoria'])
        except Exception:
            categoria = 'livre'

        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("INSERT INTO banco_videos (titulo, descricao, url, categoria) VALUES (?, ?, ?, ?)", (titulo, descricao, url, categoria))
        con.commit()
        video_id = cur.lastrowid
        con.close()

        result = {
            'ID': video_id,
            'Titulo': video_data['titulo'],
            'Descricao': video_data['descricao'],
            'Url': video_data['url'],
            'Categoria': categoria
        }
        return result

    def deletarVideo(video_id):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        try:
            cur.execute(f"DELETE FROM banco_videos WHERE id={video_id}")
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
            titulo = str(video_data['titulo'])
            descricao = str(video_data['descricao'])
            url = str(video_data['url'])
        except KeyError as e:
            return {'alerta': f'Campo ausente: {e.args[0]}'}

        if not titulo or not titulo.strip() or not descricao or not descricao.strip() or not url or not url.strip():
            return {'alerta': 'Os campos devem ser preenchidos corretamente.'}

        if requests.get(url).status_code == 400:
            return {'alerta': 'URL indisponível'}
        
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("UPDATE banco_videos SET titulo=?, descricao=?, url=? WHERE id=?", (titulo, descricao, url, video_id))
        con.commit()

        cur.execute(f"SELECT * FROM banco_videos WHERE ID = {video_id}")
        videos = cur.fetchall()

        if videos:
            for video in videos:
                cur.execute("SELECT cor FROM banco_categoria WHERE titulo=?", (video[4],))
                cor = cur.fetchone()
                
                result = {
                    "id": video[0],
                    "titulo": video[1],
                    "descricao": video[2],
                    "categoria": video[4],
                    "cor": cor[0] if cor else None,
                    "url": video[3]
                }
        
        else:
            result = {
                'alerta': 'Video não encontrado!'
            }

        con.close()
        return result

    def atualizarCampoVideo(video_id, campo, dados_campo):
        try:
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()

            cur.execute(f"UPDATE banco_videos SET {campo}=? WHERE id=?", (dados_campo, video_id))
            con.commit()
            
            cur.execute("SELECT * FROM banco_videos WHERE id=?", (video_id,))
            videos = cur.fetchall()

            result = []
            if videos:
                for video in videos:
                    cur.execute("SELECT cor FROM banco_categoria WHERE titulo=?", (video[4],))
                    cor = cur.fetchone()
                    
                    video_data = {
                        "id": video[0],
                        "titulo": video[1],
                        "descricao": video[2],
                        "categoria": video[4],
                        "cor": cor[0] if cor else None,
                        "url": video[3]
                    }

                    result.append(video_data)

            else:
                result = {
                    'alerta': 'Video não encontrado!'
                }

            con.close()        
            return result

        except Exception as error:
            result = {"alerta": f"{str(error)}"}

        return result

    # Funcoes para categorias 
    def listandoCategorias():
        """ Listando os videos e informações """

        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("SELECT * FROM banco_categoria")
        categorias = cur.fetchall()
        
        result = []

        if categorias:
            for categoria in categorias:
                categoria_info = {
                    "id": categoria[0],
                    "titulo": categoria[1],
                    "cor": categoria[2]
                }
                result.append(categoria_info)
        
        else:
            result = {
                'alerta': 'Categoria não encontrada!'
            }

        con.close()
        return result

    def videoCtgr(categoria_id, categoria_titulo):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()

        if categoria_id:
            cur.execute("SELECT titulo FROM banco_categoria WHERE id=?", (categoria_id,))
            categoria_banco = cur.fetchone()
            if categoria_banco:
                categoria = categoria_banco[0]
            else:
                result = {
                    'alerta': 'Categoria não encontrada!'
                }
                return result

        elif categoria_titulo:
            categoria = categoria_titulo

        cur.execute(f"SELECT * FROM banco_videos WHERE categoria = ?", (categoria,))
        videos = cur.fetchall()

        result = []

        if videos:
            for video in videos:
                cur.execute("SELECT cor FROM banco_categoria WHERE titulo=?", (video[4],))
                cor = cur.fetchone()
                
                video_data = {
                    "id": video[0],
                    "titulo": video[1],
                    "descricao": video[2],
                    "categoria": video[4],
                    "cor": cor[0] if cor else None,
                    "url": video[3]
                }

                result.append(video_data)

        else:
            result = {
                'alerta': 'Video não encontrado!'
            }

        con.close()
        return result


    def selecionarCategoria(categoria_id):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM banco_categoria WHERE ID = {categoria_id}")
        categorias = cur.fetchall()

        if categorias:
            for categoria in categorias:
                result = {
                    "id": categoria[0],
                    "titulo": categoria[1],
                    "cor": categoria[2]
                }
                return result
        
        else:
            result = {
                'alerta': 'Categoria não encontrada!'
            }

        con.close()
        return result  
    
    def adicionarCategoria(categoria_data):
        if not isinstance(categoria_data, dict):
            return {'erro': 'Dados inválidos. Esperado um dicionário JSON.'}
        try:
            titulo = str(categoria_data['titulo'])
            cor = str(categoria_data['cor'])

        except KeyError as e:
            return {'alerta': f'Campo ausente: {e.args[0]}'}
        
        if not titulo.strip() or not cor.strip():
            return {'alerta': 'Os campos devem ser preenchidos corretamente.'}
        
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("INSERT INTO banco_categoria (titulo, cor) VALUES (?, ?)", (titulo, cor))
        con.commit()
        categoria_id = cur.lastrowid
        con.close()

        result = {
            'ID': categoria_id,
            'Titulo': str(categoria_data['titulo']),
            'Descricao': str(categoria_data['cor'])
        }
        return result

    def deletarCategoria(categoria_id):
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM banco_categoria WHERE id=?",(categoria_id,))
            con.commit()
            result = {'alerta': 'Categoria deletada com sucesso!'}
            return result
        except Exception as error:
            error = str(error)
            result = {'alerta': f'{error}'}
            return result

    def autalizarCategoria(categoria_id, categoria_data):
        if not isinstance(categoria_data, dict):
            return {'erro': 'Dados inválidos. Esperado um dicionário JSON.'}
        try:
            titulo = str(categoria_data['titulo'])
            cor = str(categoria_data['cor'])
        except KeyError as e:
            return {'alerta': f'Campo ausente: {e.args[0]}'}

        if not titulo or not titulo.strip() or not cor.strip():
            return {'alerta': 'Os campos devem ser preenchidos corretamente.'}
        
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("UPDATE banco_categoria SET titulo=?, cor=? WHERE id=?", (titulo, cor, categoria_id))
        con.commit()

        cur.execute("SELECT * FROM banco_categoria WHERE ID =?", (categoria_id,))
        rows = cur.fetchall()

        if rows:
            for categoria in rows:
                result = {
                    "id": categoria[0],
                    "titulo": categoria[1],
                    "cor": categoria[2]
                }
        
        else:
            result = {
                'alerta': 'Categoria não encontrada!'
            }
            
        con.close()
        return result
    
    def atualizarCampoCategoria(categoria_id, campo, dados_campo):
        try:
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute(f"UPDATE banco_categoria SET {campo}=? WHERE id=?",(dados_campo, categoria_id,))
            con.commit()

            cur.execute(f"SELECT * FROM banco_categoria WHERE ID = ?", (categoria_id,))
            categorias = cur.fetchall()
            result = []

            if categorias:
                for categoria in categorias:
                    
                    categoria_data = {
                        "id": categoria[0],
                        "titulo": categoria[1],
                        "descricao": categoria[2]
                    }

                    result.append(categoria_data)

            else:
                result = {
                    'alerta': 'Categoria não encontrada!'
                }

            con.close()        
            return result

        except Exception as error:
            result = {"alerta": f"{str(error)}"}

        return result