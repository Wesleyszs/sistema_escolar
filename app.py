from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='USUARIO', #coloque o usuario do seu banco 
            password='SENHA', #coloque a senha do seu banco 
            database='escola'
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def inserir_aluno(id, nome, data_nascimento, endereco, telefone, email):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO Alunos (id, nome, data_nascimento, endereco, telefone, email) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, nome, data_nascimento, endereco, telefone, email))
            conexao.commit()
            print("Aluno inserido com sucesso")
        except Error as e:
            print(f"Erro ao inserir aluno: {e}")
        finally:
            cursor.close()
            conexao.close()

def inserir_disciplina(nome):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO Disciplinas (nome) VALUES (%s)"
            cursor.execute(sql, (nome,))
            conexao.commit()
            print("Disciplina inserida com sucesso")
        except Error as e:
            print(f"Erro ao inserir disciplina: {e}")
        finally:
            cursor.close()
            conexao.close()

def inserir_professor(nome, disciplina, email, telefone):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO Professores (nome, disciplina, email, telefone) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, disciplina, email, telefone))
            conexao.commit()
            print("Professor inserido com sucesso")
        except Error as e:
            print(f"Erro ao inserir professor: {e}")
        finally:
            cursor.close()
            conexao.close()

def inserir_nota(aluno_id, disciplina_id, nota):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT nome FROM Alunos WHERE id = %s", (aluno_id,))
            aluno_nome = cursor.fetchone()[0]
            cursor.execute("SELECT nome FROM Disciplinas WHERE id = %s", (disciplina_id,))
            disciplina_nome = cursor.fetchone()[0]
            sql = "INSERT INTO Notas (aluno_id, disciplina_id, nota, nome_aluno, nome_disciplina) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (aluno_id, disciplina_id, nota, aluno_nome, disciplina_nome))
            conexao.commit()
            print("Nota inserida com sucesso")
        except Error as e:
            print(f"Erro ao inserir nota: {e}")
        finally:
            cursor.close()
            conexao.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alunos')
def alunos():
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Alunos")
        alunos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return render_template('alunos.html', alunos=alunos)
    return "Erro ao conectar ao banco de dados"

@app.route('/adicionar_aluno', methods=['POST'])
def adicionar_aluno():
    id = request.form['id']
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    inserir_aluno(id, nome, data_nascimento, endereco, telefone, email)
    return redirect(url_for('alunos'))

@app.route('/disciplinas')
def disciplinas():
    conexao = criar_conexao()
    if (conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Disciplinas")
        disciplinas = cursor.fetchall()
        cursor.close()
        conexao.close()
        return render_template('disciplinas.html', disciplinas=disciplinas)
    return "Erro ao conectar ao banco de dados"

@app.route('/adicionar_disciplina', methods=['POST'])
def adicionar_disciplina():
    nome = request.form['nome']
    inserir_disciplina(nome)
    return redirect(url_for('disciplinas'))

@app.route('/professores')
def professores():
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Professores")
        professores = cursor.fetchall()
        cursor.close()
        conexao.close()
        return render_template('professores.html', professores=professores)
    return "Erro ao conectar ao banco de dados"

# Função para deletar aluno
def deletar_aluno(aluno_id):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM Alunos WHERE id = %s"
            cursor.execute(sql, (aluno_id,))
            conexao.commit()
            print("Aluno deletado com sucesso")
        except Error as e:
            print(f"Erro ao deletar aluno: {e}")
        finally:
            cursor.close()
            conexao.close()

@app.route('/deletar_aluno/<int:aluno_id>', methods=['POST'])
def deletar_aluno_route(aluno_id):
    deletar_aluno(aluno_id)
    return redirect(url_for('alunos'))

# Função para deletar disciplina
def deletar_disciplina(disciplina_id):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM Disciplinas WHERE id = %s"
            cursor.execute(sql, (disciplina_id,))
            conexao.commit()
            print("Disciplina deletada com sucesso")
        except Error as e:
            print(f"Erro ao deletar disciplina: {e}")
        finally:
            cursor.close()
            conexao.close()

@app.route('/deletar_disciplina/<int:disciplina_id>', methods=['POST'])
def deletar_disciplina_route(disciplina_id):
    deletar_disciplina(disciplina_id)
    return redirect(url_for('disciplinas'))

# Função para deletar professor
def deletar_professor(professor_id):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM Professores WHERE id = %s"
            cursor.execute(sql, (professor_id,))
            conexao.commit()
            print("Professor deletado com sucesso")
        except Error as e:
            print(f"Erro ao deletar professor: {e}")
        finally:
            cursor.close()
            conexao.close()

@app.route('/deletar_professor/<int:professor_id>', methods=['POST'])
def deletar_professor_route(professor_id):
    deletar_professor(professor_id)
    return redirect(url_for('professores'))

# Função para deletar nota
def deletar_nota(nota_id):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM Notas WHERE id = %s"
            cursor.execute(sql, (nota_id,))
            conexao.commit()
            print("Nota deletada com sucesso")
        except Error as e:
            print(f"Erro ao deletar nota: {e}")
        finally:
            cursor.close()
            conexao.close()

@app.route('/deletar_nota/<int:nota_id>', methods=['POST'])
def deletar_nota_route(nota_id):
    deletar_nota(nota_id)
    return redirect(url_for('notas'))


@app.route('/adicionar_professor', methods=['POST'])
def adicionar_professor():
    nome = request.form['nome']
    disciplina = request.form['disciplina']
    email = request.form['email']
    telefone = request.form['telefone']
    inserir_professor(nome, disciplina, email, telefone)
    return redirect(url_for('professores'))

def inserir_nota(aluno_id, disciplina_id, nota):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT nome FROM Alunos WHERE id = %s", (aluno_id,))
            aluno_nome = cursor.fetchone()[0]
            cursor.execute("SELECT nome FROM Disciplinas WHERE id = %s", (disciplina_id,))
            disciplina_nome = cursor.fetchone()[0]
            sql = "INSERT INTO Notas (aluno_id, disciplina_id, nota, nome_aluno, nome_disciplina) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (aluno_id, disciplina_id, nota, aluno_nome, disciplina_nome))
            conexao.commit()
            print("Nota inserida com sucesso")
        except Error as e:
            print(f"Erro ao inserir nota: {e}")
        finally:
            cursor.close()
            conexao.close()
            
@app.route('/notas', methods=['GET', 'POST'])
def notas():
    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        disciplina_id = request.form['disciplina_id']
        nota = request.form['nota']
        inserir_nota(aluno_id, disciplina_id, nota)
        return redirect(url_for('notas'))
    
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("""
                SELECT Notas.id, Alunos.nome AS aluno_nome, Disciplinas.nome AS disciplina_nome, Notas.nota
                FROM Notas
                JOIN Alunos ON Notas.aluno_id = Alunos.id
                JOIN Disciplinas ON Notas.disciplina_id = Disciplinas.id
            """)
            notas = cursor.fetchall()
            cursor.close()
            conexao.close()
            return render_template('notas.html', notas=notas)
        except Error as e:
            print(f"Erro ao executar a consulta SQL: {e}")
            return "Erro ao recuperar os dados das notas"
    return "Erro ao conectar ao banco de dados"


@app.route('/adicionar_nota', methods=['POST'])
def adicionar_nota():
    aluno_id = request.form['aluno_id']
    disciplina_id = request.form['disciplina_id']
    nota = request.form['nota']
    inserir_nota(aluno_id, disciplina_id, nota)
    return redirect(url_for('notas'))

if __name__ == '__main__':
    app.run(debug=False)

