from flask import Flask, render_templete

app = Flask(__name__)

@app.route('/')
def home(): 
    return render_templete('home.html')

@app.route('/sobre/<nome>')
def sobre(nome):
    return f'Olá,{nome}! Bem vindo à página.'

if __name__=='__main__': 
    app.run(debug=True)