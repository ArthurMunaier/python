from flask import Flask

app = Flask(__name__)

@app.route('home')
def home(): 
    return render_templete('indexMarte.html')














if __name__ == "__main__":
    app.run(debug=True)
