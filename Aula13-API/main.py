from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/marte')
def page1():
    return render_template('marte.html')

@app.route('/espaco')
def page2():
    return render_template('espaco.html')

@app.route('/buracoNegro')
def page3():
    return render_template('buracoNegro.html')

if __name__ == '__main__':
    app.run(debug=True)
