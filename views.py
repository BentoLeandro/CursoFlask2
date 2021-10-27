from flask import render_template, request, redirect, session, flash, url_for, send_from_directory 
from models import Jogo
from dao import JogoDao, UsuarioDao

import time
from helpers import deleta_imagens_antigas, recupera_imagem, deleta_imagens_antigas
from app import app, db

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
@app.route('/inicio')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos!', jogos=lista)

@app.route('/novo')
def novo():    
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:    
        return render_template('novo.html', titulo='Novo Jogo Teste')    

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    #lista.append(jogo)
    jogo = jogo_dao.salvar(jogo)

    upload_path = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa_{jogo.id}_{timestamp}.jpg')
    return redirect(url_for('index'))  #render_template('lista.html', titulo='Jogos!', jogos=lista)

@app.route('/editar/<int:id>')
def editar(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login', proxima=url_for('editar')))
    else:    
        jogo = jogo_dao.buscar_por_id(id)
        #capa = f'capa_{id}.jpg'
        nome_imagem = recupera_imagem(id)
        return render_template('editar.html', titulo='Editar Informações do Jogo', 
                                jogo=jogo, capa_jogo=nome_imagem)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    id = request.form['id']
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=id)
    jogo_dao.salvar(jogo) 

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_imagens_antigas(jogo.id)
    arquivo.save(f'{upload_path}/capa_{jogo.id}_{timestamp}.jpg')

    return redirect(url_for('index'))       

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index')) 

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima_pg=proxima)

@app.route('/logout')
def logout():
    if session['usuario_logado'] != '':
        session['usuario_logado'] = None

    flash('Usuário foi deslogado...')
    return redirect(url_for('index'))    

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            pagina = request.form['proxima']
            flash(usuario.nome+' Logou com sucesso!')
            return redirect(pagina) #'/{}'.format(pagina) 
        else:
            flash('Senha do usuário está Errada!') 
            return redirect(url_for('login'))                          
    else:
        flash('Usuário não localizado na Base! Tente novamente!')
        return redirect(url_for('login'))  

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

