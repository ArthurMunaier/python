from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def q1():
     return render_template('q1.html', name = "Arthur Munaier")
 
 
@app.route ("/2")
def q2():
     nome = "Arthur Munaier" 
     idade = 17
     return render_template('q2.html', nome=nome, idade=idade)
 
@app.route ("/3")
def q3():
     nome = "Arthur Munaier" 
     email = "22502122@aluno.cotemig.com.br"
     return render_template('q3.html', nome=nome, email=email)

@app.route ("/4")
def q4():
     lista = {"Arthur", "Dudu", "Lucas", "Yaslan" }
     return render_template('q4.html', lista=lista)


@app.route('/nota')
def notas():
    alunos = [
        {'nome': 'Ana', 'notas': 8.5},
        {'nome': 'Bruno','notas': 7.0},
        {'nome': 'Carlos','notas': 9.0},
        {'nome': 'Diana','notas': 6.5}
    ]
    return render_template('nota.html' , notas=alunos )





if __name__ == "__main__":
    app.run(debug=True)
