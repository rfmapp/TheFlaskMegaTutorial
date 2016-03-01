# -*- coding: utf-8 -*-
# Aqui importamos a classe Form
from flask.ext.wtf import Form
# Aqui importamos os dois campos que iremos utilizar
from wtforms import StringField, BooleanField
# Aqui importamos um validador, que vai checar se o campo não está vazio.
from wtforms.validators import DataRequired

# Criamos nosso formulário.
class LoginForm(Form):
    # Aqui temos o campo para entrar com o OpenId.
    openid = StringField('openid', validators=[DataRequired()])
    # Aqui temos uma checkbox para saber se o usuário quer ser lembrado.
    remember_me = BooleanField('remember_me', default=False)
