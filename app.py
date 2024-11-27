import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash   


app = Flask(__name__)   


# URL de conexão interna fornecida pelo Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pet_d2gc_user:JhoUoF7zYeyL4dvj0Pu28JZ95rbdQtTB@dpg-ct3n2apu0jms73a2fopg-a.oregon-postgres.render.com/pet_d2gc'  
app.config['SECRET_KEY'] = '2236'  # Substitua por uma chave secreta forte
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    ddd = db.Column(db.String(2), nullable=False)
    telefone = db.Column(db.String(9), nullable=False)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    quantidade = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.String(200))
    unidade_medida = db.Column(db.String(20))
    vencimento = db.Column(db.String(10), nullable=False)  # Formato: YYYY-MM-DD
    especie_pet = db.Column(db.String(20))
    disponivel = db.Column(db.Boolean, default=True)  # Disponibilidade do produto
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', backref='produtos')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        ddd = request.form['ddd']
        telefone = request.form['telefone']
        senha = request.form['senha']
        senha_confirmacao = request.form['senha_confirmacao']

        if senha != senha_confirmacao:
            flash('As senhas não coincidem!', 'error')
            return redirect(url_for('cadastro'))

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            flash('Email já cadastrado!', 'error')
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, ddd=ddd, telefone=telefone, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            return redirect(url_for('principal', usuario_id=usuario.id))
        else:
            flash('Email ou senha inválidos!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/principal/<int:usuario_id>')
def principal(usuario_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.get(usuario_id)
    produtos = Produto.query.filter_by(usuario_id=usuario_id).all()

    return render_template('index.html', usuario=usuario, produtos=produtos)


@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))


@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        observacao = request.form['observacao']
        quantidade = request.form['quantidade']
        vencimento = request.form['vencimento']
        unidade_medida = request.form['unidade_medida']
        especie_pet = request.form['especie_pet']
        disponivel = 'disponivel' in request.form

        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            observacao=observacao,
            quantidade=quantidade,
            unidade_medida=unidade_medida,
            vencimento=vencimento,
            especie_pet=especie_pet,
            disponivel=disponivel,
            usuario_id=session['usuario_id']
        )
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('principal', usuario_id=session['usuario_id']))

    return render_template('cadastrar_produto.html')


@app.route('/buscar_produto', methods=['GET'])
def buscar_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    nome_produto = request.args.get('nome_produto')
    especie_pet = request.args.get('especie_pet')  # Obter a espécie do pet do formulário

    query = Produto.query.filter(Produto.nome.ilike(f'%{nome_produto}%')) 

    if especie_pet:  # Filtrar por espécie se uma opção for selecionada
        query = query.filter(Produto.especie_pet == especie_pet)

    produtos = query.all()
    return render_template('buscar_produto.html', produtos=produtos, usuario_id=session['usuario_id'])


@app.route('/alterar_disponibilidade/<int:produto_id>', methods=['GET'])
def alterar_disponibilidade(produto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    produto = Produto.query.get_or_404(produto_id)

    if produto.usuario_id != session['usuario_id']:
        flash('Você não tem permissão para alterar este produto.', 'error')
        return redirect(url_for('principal', usuario_id=session['usuario_id']))

    produto.disponivel = not produto.disponivel
    db.session.commit()

    return redirect(url_for('principal', usuario_id=session['usuario_id']))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)