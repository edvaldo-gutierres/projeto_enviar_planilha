from flask import Flask, render_template, request, g, redirect, session, flash, url_for
import os
import openpyxl
import sqlite3


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome=nome
        self.nickname=nickname
        self.senha=senha

usuario1 = Usuario('edvaldo', 'ed', '12345')
usuario2 = Usuario('carlos','carlos', 'vital123')
usuario3 = Usuario('gilson', 'gil', 'vital321')

usuarios = {usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3}


app = Flask(__name__)
app.secret_key = 'b*i;XP0$5fghjaLkJH%586'  # Defina sua chave secreta


# Cria uma pasta para salvar os uploads
if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route('/inicio')
def inicio():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('inicio')))
    return render_template('inicio.html')


@app.route('/')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            return redirect(url_for('inicio'))  # Redireciona para a rota /inicio
        else:
            flash('Senha incorreta!')
            return redirect(url_for('login'))
    else:
        flash('Usuário não encontrado!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


# Conexão com o banco de dados SQLite
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('grupovital.db')
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Rota para exibir o formulário
@app.route('/enviar')
def enviar():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('enviar')))
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html')

# Rota para receber o arquivo e processá-lo
@app.route('/upload', methods=['POST'])
def upload_file():
    excel_file = request.files['excel_file']

    if excel_file.filename != '':
        file_path = os.path.join('uploads', excel_file.filename)
        excel_file.save(file_path)

        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            nome_empresa, ano, faturamento = row
            data.append((nome_empresa, ano, faturamento))

        db = get_db()
        cursor = db.cursor()
        for row in data:
            nome_empresa, ano, faturamento = row
            cursor.execute("INSERT INTO planilha (nome_empresa, ano, faturamento) VALUES (?, ?, ?)",
                           (nome_empresa, ano, faturamento))
        db.commit()

        os.remove(file_path)

        return redirect(url_for('result'))
    else:
        return "Nenhum arquivo enviado."


if __name__ == '__main__':
    app.run(debug=True)
