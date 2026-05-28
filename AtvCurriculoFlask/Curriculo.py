from flask import Flask

app = Flask(__name__)

@app.route("/")
def curriculo(): 
    return '''    
    
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Currículo - Arthur Munaier</title>
    </head>
    <body>
        <h1>Currículo<h1>

        <h3>Informações pessoais<h3>
        <ul>
            <li>Nome: Arthur Augusto Bittencort Munaier</li>
            <li>Email:22502122@aluno.cotemig.com.br</li>
            <li>Número: (+55) 31 95467-9072</li>
            
          </ul>

          <h3>Nivel escolar<h3>

          <ul>
          <li> Escolaridade: Cursando 3º </li>
          </ul>

          <h3>Habilidades<h3>

          <ul>
          <li>Comunicativo</li>
          <li>Flexivel</li>


          </ul>

'''


if __name__ == "__main__":
    app.run(debug=True)
