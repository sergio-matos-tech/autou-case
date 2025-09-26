
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():

    return "Olá, Mundo! Servidor da AutoU no ar."


if __name__ == '__main__':
    app.run(debug=True)