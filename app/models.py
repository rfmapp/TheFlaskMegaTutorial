# -*- coding: utf-8 -*-

# Importamos o objeto db do módulo que criamos.
from app import db

# Criamos a classe que representa a tabela de usuários.
class User(db.Model):
    # Campo 'id', do tipo 'integer' e que também é a chave primária.
    id = db.Column(db.Integer, primary_key = True)
    # Campo 'nickname', do tipo 'string', com limite de 64 caracteres, indexado
    # e único.
    nickname = db.Column(db.String(64), index = True, unique = True)
    # Campo 'email', do tipo 'string', com limite de 120 caracteres, indexado
    # e único.
    email = db.Column(db.String(120), index = True, unique = True)
    # Este é um 'campo oculto', por assim dizer. Ele existe apenas para definir
    # o relacionamento existente entre as tabelas 'User' e 'Post'. Assim temos
    # os argumentos 'Post', que é a tabela a que se refere, 'backref', que é o
    # referencial local do campo da tabela a que se refere, no caso 'user_id'
    # e por fim 'lazy', que ....
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    # Método que indica como exibir objetos dessa classe. Será usado para debug.
    def __repr__(self):
        return '<User %r>' % (self.nickname)

# Criamos a classe que representa a tabela de posts dos usuários.
class Post(db.Model):
    # Campo 'id', do tipo 'integer' e que também é a chave primária.
    id = db.Column(db.Integer, primary_key = True)
    # Campo 'body', do tipo 'string', com limite de 140 caracteres.
    body = db.Column(db.String(140))
    # Campo 'timestamp', do tipo 'DateTime'.
    timestamp = db.Column(db.DateTime)
    # Campo 'user_id', do tipo 'integer' e que também é chave estrangeira.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Método que indica como exibir objetos dessa classe. Será usado para debug.
    def __repr__(self):
        return '<Post %r>' % (self.body)
