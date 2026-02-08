from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_aleatoria'

DATABASE = 'tarefas.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            custo REAL NOT NULL,
            data_limite DATE NOT NULL,
            ordem_apresentacao INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tarefas ORDER BY ordem_apresentacao")
    tarefas = cursor.fetchall()
    conn.close()
    total = sum(t['custo'] for t in tarefas)
    return render_template('index.html', tarefas=tarefas, total=total)

@app.route('/incluir', methods=['POST'])
def nova_tarefa():
    if request.method == 'POST':
        nome = request.form['nome']
        try:
            custo = float(request.form['custo'])
        except ValueError:
            custo = 0.0
        data_limite = request.form['data_limite']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(ordem_apresentacao) as max_ordem FROM Tarefas")
        resultado = cursor.fetchone()
        nova_ordem = 1
        if resultado['max_ordem'] is not None:
            nova_ordem = resultado['max_ordem'] + 1
            
        try:
            cursor.execute("INSERT INTO Tarefas (nome, custo, data_limite, ordem_apresentacao) VALUES (?, ?, ?, ?)", 
                           (nome, custo, data_limite, nova_ordem))
            conn.commit()
        except sqlite3.IntegrityError:
            flash(f'Erro: A tarefa "{nome}" já existe!', 'error')
        finally:
            conn.close()
        return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar_tarefa(id):
    nome = request.form['nome']
    try:
        custo = float(request.form['custo'])
    except ValueError:
        custo = 0.0
    data_limite = request.form['data_limite']
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Tarefas SET nome = ?, custo = ?, data_limite = ? WHERE id = ?", 
                       (nome, custo, data_limite, id))
        conn.commit()
    except sqlite3.IntegrityError:
        flash(f'Erro: Já existe outra tarefa com o nome "{nome}"!', 'error')
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir_tarefa(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/subir/<int:id>')
def subir_tarefa(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ordem_apresentacao FROM Tarefas WHERE id = ?", (id,))
    tarefa_atual = cursor.fetchone()
    if tarefa_atual:
        cursor.execute("SELECT id, ordem_apresentacao FROM Tarefas WHERE ordem_apresentacao < ? ORDER BY ordem_apresentacao DESC LIMIT 1", (tarefa_atual['ordem_apresentacao'],))
        tarefa_acima = cursor.fetchone()
        if tarefa_acima:
            conn.execute("UPDATE Tarefas SET ordem_apresentacao = -1 WHERE id = ?", (id,))
            conn.execute("UPDATE Tarefas SET ordem_apresentacao = ? WHERE id = ?", (tarefa_atual['ordem_apresentacao'], tarefa_acima['id']))
            conn.execute("UPDATE Tarefas SET ordem_apresentacao = ? WHERE id = ?", (tarefa_acima['ordem_apresentacao'], id))
            conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/descer/<int:id>')
def descer_tarefa(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ordem_apresentacao FROM Tarefas WHERE id = ?", (id,))
    tarefa_atual = cursor.fetchone()
    if tarefa_atual:
        cursor.execute("SELECT id, ordem_apresentacao FROM Tarefas WHERE ordem_apresentacao > ? ORDER BY ordem_apresentacao ASC LIMIT 1", (tarefa_atual['ordem_apresentacao'],))
        tarefa_abaixo = cursor.fetchone()
        if tarefa_abaixo:
            conn.execute("UPDATE Tarefas SET ordem_apresentacao = -1 WHERE id = ?", (id,))
            conn.execute("UPDATE Tarefas SET ordem_apresentacao = ? WHERE id = ?", (tarefa_atual['ordem_apresentacao'], tarefa_abaixo['id']))
            conn.execute("UPDATE Tarefas SET ordem_apresentacao = ? WHERE id = ?", (tarefa_abaixo['ordem_apresentacao'], id))
            conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/reordenar', methods=['POST'])
def reordenar():
    try:
        dados = request.get_json()
        id_list = dados['ordem']
        conn = get_db()
        cursor = conn.cursor()
        for index, tarefa_id in enumerate(id_list):
            cursor.execute("UPDATE Tarefas SET ordem_apresentacao = ? WHERE id = ?", (index + 1, tarefa_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)