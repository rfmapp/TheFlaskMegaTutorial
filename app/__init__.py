# -*- coding: utf-8 -*-

# Aqui importamos o módulo para funções de sistema operacional.
import os
# Aqui importamos a classe Flask.
from flask import Flask
# Aqui importamos a classe SQLAlchemy.
from flask.ext.sqlalchemy import SQLAlchemy
# Aqui importamos a classe 'LoginManager'.
from flask.ext.login import LoginManager
# Aqui importamos a classe 'OpenId'.
from flask.ext.openid import OpenId
# Aqui importamos o objeto 'basedir' do nosso arquivo de configuração.
from config import basedir

# Aqui criamos um objeto (app) da classe Flask.
app = Flask(__name__)
# Aqui informamos que nossa aplicação requer o arquivo de configuração.
app.config.from_object('config')
# Aqui criamos o objeto que representará o banco de dados.
db = SQLAlchemy(app)
# Aqui criamos o objeto da classe 'LoginManager'.
lm = LoginManager()
# Aqui indicamos nossa aplicação para o objeto.
lm.init_app(app)
# A extensão 'OpenId' requer que seja indicado um caminho para um diretório
# temporário onde arquivos possam ser armazenados.
oid = OpenId(app, os.path.join(basedir, 'tmp'))

# Aqui importamos os módulos 'views' e 'models' do pacote 'app'. Esse import
# está localizado no final do arquivo e não no início como de costume porque
# precisamos evitar uma referência circular, já que os módulos irão importar
# variáveis definidas aqui.
from app import views, models
