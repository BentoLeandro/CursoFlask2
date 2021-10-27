import os
from app import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo   

    return ''

def deleta_imagens_antigas(id):
    arquivo = recupera_imagem(id)
    if arquivo != '': 
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
