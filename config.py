# -*- coding: utf-8 -*-
# O arquivo de configuração da aplicação.

# Importamos pacote para trabalhar com funções de sistema operacional
import os

# Criamos objeto com o caminho da aplicação.
basedir = os.path.abspath(os.path.dirname(__file__))
# Indicamos o caminho para o banco de dados.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# Indicamos o caminho para o diretório em que armazenaremos os arquivos de
# dados de migração do banco de dados.
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Aqui definimos que queremos habilitar a proteção CSRF.
WTF_CSRF_ENABLED = True
# Aqui definimos uma chave para a proteção.
SECRET_KEY = "diga-amigo-e-entre"

# Definimos a lista de provedores de 'OpenIds' que teremos em nosso sistema.
OPENID_PROVIDERS = [
    {'name': 'StackExchange', 'url': 'https://openid.stackexchange.com'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenId', 'url': 'https://www.myopenid.com'}
]
