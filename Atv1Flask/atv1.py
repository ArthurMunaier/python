from flask import Flask 

app = Flask(__name__)

@app.route("/")
def menu(): 
    return "Hello"

@app.route("/decorator")
def arthur(): 
    return '''Decoradores em Python são funções que modificam ou estendem o comportamento de outras funções ou classes sem alterar seu código-fonte original <br>
    Um decorator em Python serve para modificar ou estender o comportamento de funções ou classes de forma reutilizável e limpa, sem alterar seu código original.<br>

    O decorador @app.route() no Flask é utilizado para mapear URLs (endereços web) a funções específicas do Python, definindo o que deve acontecer quando um usuário acessa um determinado caminho no navegador. Ele transforma uma função Python comum em uma "view" (exibição) web.
    
    '''
    

if __name__ == "__main__":
    app.run(debug=True)
