# -*- coding: utf-8 -*-

# Importamos o objeto db do módulo que criamos.
from app import db
# Importamos a função 'md5'.
from hashlib import md5

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
    # Campo 'about_me', do tipo string, com limite de 140 caracteres.
    about_me = db.Column(db.String(140))
    # Campo 'last_seen', do tipo 'DateTime'.
    last_seen = db.Column(db.DateTime)

    # Em geral, esse método deve apenas retornar verdadeiro a menos que o objeto
    # represente um usuário que não tenha permissão para autenticar.
    @property
    def is_authenticated(self):
        return True

    # Deve retornar verdadeiro a menos que o usuário não esteja ativo. Por
    # exemplo, se ele tiver sido banido.
    @property
    def is_active(self):
        return True

    # Deve retornar verdadeiro para usuários falsos, que não devem logar no
    # sistema.
    @property
    def is_anonymous(self):
        return False

    # Retorna o id do usuário em formato unicode.
    def get_id(self):
        return unicode(self.id)

    # Método que indica como exibir objetos dessa classe. Será usado para debug.
    def __repr__(self):
        return '<User %r>' % (self.nickname)

    # Método que importa o avatar do serviço 'Gravatar'.
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

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
