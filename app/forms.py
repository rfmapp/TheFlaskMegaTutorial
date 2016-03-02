# -*- coding: utf-8 -*-
# Aqui importamos a classe Form
from flask.ext.wtf import Form
# Aqui importamos os campos de formulário que iremos utilizar.
from wtforms import StringField, BooleanField, TextAreaField
# Aqui importamos um validadores.
from wtforms.validators import DataRequired, Length

# Formulário de login.
class LoginForm(Form):
    # Aqui temos o campo para entrar com o OpenId.
    openid = StringField('openid', validators=[DataRequired()])
    # Aqui temos uma checkbox para saber se o usuário quer ser lembrado.
    remember_me = BooleanField('remember_me', default=False)

# Formulário de edição de dados do usuário.
class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
