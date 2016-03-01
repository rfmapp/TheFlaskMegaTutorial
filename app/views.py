# -*- coding: utf-8 -*-
# Aqui importamos a função 'render_template', 'flash' e 'redirect',
# do pacote 'flask'.
from flask import render_template, flash, redirect
# Aqui importamos o objeto 'app' do pacote de mesmo nome.
from app import app
# Aqui importamos  a classe LoginForm.
from .forms import LoginForm

# Definimos nossas rotas principais, para a página inicial do sistema.
@app.route('/')
@app.route('/index')

# Função para a página inicial.
def index():
    # Obtemos o nome de usuário que está logando no sistema.
    user = {'nickname': 'Miguel'} # fake user
    # Obtemos a lista de posts já feitos, com o autor e corpo do post.
    posts = [ # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    # Retornamos ao usuário a página inicial, com o título da página, usuário
    # e lista de posts.
    return render_template('index.html',
                           title = 'Home',
                           user = user,
                           posts = posts)

# Definimos a rota para o formulário de login, com o argumento 'methods', que
# indica ao Flask que a view aceita requisições dos tipos GET e POST. Sem isso,
# a view aceitaria apenas requisições GET, que é o padrão. Já que teremos dados
# sendo enviados pelo usuário, precisamos das requisições do tipo POST.
@app.route('/login', methods=['GET', 'POST'])

# Função para a página de login.
def login():
    # Criação do objeto da classe LoginForm.
    form = LoginForm()
    # Aqui é onde ocorre todo o processamento do formulário.
    if form.validate_on_submit():
        # Se a validação é bem sucedida, é apresentada uma mensagem ao usuário
        # informando e liberando seu acesso.
        flash('Login requested for OpenId="%s", remember_me=%s' %
                (form.openid.data, str(form.remember_me.data)))
        # Aqui fazemos o direcionamento do usuário logado.
        return redirect('/index')
    # Retornamos ao usuário a página de login, com o título da página, o objeto
    # form e a lista de provedores de OpenId.
    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])
