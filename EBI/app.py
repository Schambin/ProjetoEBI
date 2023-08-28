from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-cpf/<cpf>', methods=['GET'])
def check_cpf(cpf):
    connection = sqlite3.connect('cpf_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT EXISTS (SELECT 1 FROM cpf WHERE cpf = ?)', (cpf,))
    exists = cursor.fetchone()[0] == 1
    connection.close()
    return jsonify({'exists': exists})

@app.route('/store-cpf/<cpf>', methods=['POST'])
def store_cpf(cpf):
    connection = sqlite3.connect('cpf_database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO cpf (cpf) VALUES (?)', (cpf,))
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    connection.close()
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(debug=True)

# Conectar ao banco de dados ou criar se não existir
conn = sqlite3.connect('cpf_database.db')
cursor = conn.cursor()

# Criar a tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cpfs (
        cpf TEXT PRIMARY KEY
    )
''')

conn.commit()
conn.close()
