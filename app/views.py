# -*- coding: utf-8 -*-
# Aqui importamos as funções 'render_template', 'flash', 'redirect', 'session',
# 'url_for', 'request', e 'g' do pacote 'flask'.
from flask import render_template, flash, redirect, session, url_for, request, g
# Aqui importamos  as funções 'login_user', 'logout_user', 'current_user' e
# 'login_required'.
from flask.ext.login import login_user, logout_user, current_user, login_required
# Aqui importamos o objeto 'app' do pacote de mesmo nome.
from app import app, db, lm, oid
# Aqui importamos  as classes LoginForm e EditForm.
from .forms import LoginForm, EditForm
# Aqui importamos a classe User.
from .models import User
# Importamos a função 'datetime'.
from datetime import datetime

# Função que busca usuário com base no id passado.
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Verifica se há um usuário logado.
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

# Definimos nossas rotas principais, para a página inicial do sistema.
@app.route('/')
@app.route('/index')
# Função para a página inicial.
@login_required
def index():
    # Obtemos o nome de usuário que está logando no sistema.
    user = g.user
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
@oid.loginhandler
def login():
    # Estrutura de decisão que verifica se o usuário já está logado.
    if g.user is not None and g.user.is_authenticated:
        # Se estiver logado, redireciona para a página inicial.
        return redirect(url_for('index'))
    # Criação do objeto da classe LoginForm.
    form = LoginForm()
    # Aqui é onde ocorre todo o processamento do formulário.
    if form.validate_on_submit():
        # Armazenamos o valor definido pelo usuário na sessão.
        session['remember_me'] = form.remember_me.data
        # Aciona a função que lida com login em OpenIds.
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    # Retornamos ao usuário a página de login, com o título da página, o objeto
    # form e a lista de provedores de OpenId.
    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
# O argumento passado 'resp' fornece informações passadas pelo provedor OpenId.
def after_login(resp):
    # Verifica se foi informado algum email.
    if resp.email is None or resp.email == "":
        # Caso não tenha sido, informa ao usuário.
        flash('Invalid login. Please try again.')
        # também redireciona para a página de login.
        return redirect(url_for('login'))
    # Fazemos uma busca no banco de dados pelo email fornecido e atribuímos a
    # uma variável.
    user = User.query.filter_by(email=resp.email).first()
    # Testamos se algo foi encontrado.
    if user is None:
        # Atribuímos o valor da variável correspondente.
        nickname = resp.nickname
        # Testa se o valor atribuído é nulo ou vazio.
        if nickname is None or nickname == "":
            # Se for vazio, recebe a string correspondente ao que foi passado
            # como sendo o email até o caractere '@'.
            nickname = resp.email.split('@')[0]
        # Jogamos os valores 'nickname' e 'email' no objeto da classe User.
        user = User(nickname=nickname, email=resp.email)
        # Adicionamos o objeto à sessão.
        db.session.add(user)
        # Fazemos o commit para o banco de dados.
        db.session.commit()
    # Verificamos se a opção 'remember_me' está em sessão.
    if 'remember_me' in session:
        # Se estiver definimos o valor.
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    # Registramos o login como válido.
    login_user(user, remember = remember_me)
    # Redirecionamos para a próxima página, se tiver sido definida no request,
    # ou para a página principal em caso contrário.
    return redirect(request.args.get('next') or url_for('index'))

# Definimos a rota para o logout do sistema.
@app.route('/logout')
# Função para fazer logout do usuário.
def logout():
    logout_user()
    return redirect(url_for('index'))

# Definimos a rota para a página de perfil do usuário.
@app.route('/user/<nickname>')
# Função para apresentar a view da página de perfil.
@login_required
def user(nickname):
    # Procura no banco por um usuário que corresponda ao que foi passado.
    user = User.query.filter_by(nickname=nickname).first()
    # Testa se algum usuário foi encontrado.
    if user == None:
        # Se não houver nenhum usuário no banco que corresponda, exibe mensagem.
        flash('User %s not found.' % nickname)
        # Redireciona para a página inicial.
        return redirect(url_for('index'))
        # Se houver, busca os posts daquele usuário.
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    # Apresenta a view com o nome do usuário e seus posts.
    return render_template('user.html',
                           user=user,
                           posts=posts)

# Rota para a view de edição de dados do usuário.
@app.route('/edit', methods=['GET', 'POST'])
# Função para view de edição de dados do usuário.
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit:
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)
