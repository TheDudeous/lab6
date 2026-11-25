from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Привет, мир! (Hello World)</h1><p>Это мое первое Flask-приложение.</p>'

if __name__ == '__main__':
    app.run(debug=True)
