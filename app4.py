# Instalação inicial:
# pip install Flask SQLAlchemy Flask-Migrate

from flask import redirect, url_for
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'  # ou outro banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)


# Modelo Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50))
    classificacao = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    cor = db.Column(db.String(20))
    tamanho = db.Column(db.String(10))
    valor = db.Column(db.Integer)
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    imagem = db.Column(db.String(120)) # caminho da imagem

# Modelo Venda
class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.Integer)
    data = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo Auditoria
class Auditoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    acao = db.Column(db.String(100))
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)

# Rotas

@app.route('/')
def index():
    termo_busca = request.args.get('busca', '', type=str)

    query = Produto.query

    if termo_busca:
        busca = f"%{termo_busca}%"
        query = query.filter(
            Produto.marca.ilike(busca) |
            Produto.modelo.ilike(busca) |
            Produto.cor.ilike(busca)
        )
    produtos = query.order_by(Produto.data_entrada.desc()).all()
    return render_template('index.html', produtos=produtos, busca=termo_busca)


@app.route('/novo_produto')
def novo_produto():
    return render_template('novo_produto.html')

@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    try:
        marca = request.form['marca']
        modelo = request.form['modelo']
        classificacao = request.form.get('classificacao', '')
        cor = request.form['cor']
        tamanho = request.form['tamanho']
        valor = float(request.form['valor'])
        data_entrada_str = request.form['data_entrada']
        data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d')

        novo_produto = Produto(
            marca=marca,
            modelo=modelo,
            classificacao=classificacao,
            cor=cor,
            tamanho=tamanho,
            valor=valor,
            data_entrada=data_entrada
        )
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@app.route('/produtos', methods=['GET'])
def listar_produtos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    marca = request.args.get('marca')
    cor = request.args.get('cor')
    query = Produto.query

    if marca:
        query = query.filter(Produto.marca.ilike(f'%{marca}%'))
    if cor:
        query = query.filter(Produto.cor.ilike(f'%{cor}%'))

    produtos = query.order_by(Produto.data_entrada.desc()).paginate(page=page, per_page=per_page)
    return render_template('produtos.html', produtos=produtos)

@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        try:
            produto.marca = request.form['marca']
            produto.modelo = request.form['modelo']
            produto.classificacao = request.form.get('classificacao', '')
            produto.cor = request.form['cor']
            produto.tamanho = request.form['tamanho']
            produto.valor = float(request.form['valor'])
            data_entrada_str = request.form['data_entrada']
            produto.data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d')

            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 400

    return render_template('editar_produto.html', produto=produto)


@app.route('/excluir_produto/<int:id>', methods=['POST'])
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/venda', methods=['POST'])
def registrar_venda():
    try:
        produto_ids = request.form.getlist('produto_id[]')
        for pid in produto_ids:
            quantidade = int(request.form.get(f'quantidade_{pid}', 0))
            if quantidade > 0:
                produto = Produto.query.get(pid)
                venda = Venda(
                    produto_id=produto.id,
                    quantidade=quantidade,
                    valor=produto.valor * quantidade
                )
                db.session.add(venda)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@app.route('/auditoria', methods=['POST'])
def registrar_auditoria():
    dados = request.json
    auditoria = Auditoria(**dados)
    db.session.add(auditoria)
    db.session.commit()
    return jsonify({'mensagem':'Auditoria registrada com sucesso!'}), 201

# Execução do servidor
if __name__ == '__main__':
    app.run(debug=True)
