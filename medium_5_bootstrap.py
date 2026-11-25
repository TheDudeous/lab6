from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def bootstrap_page():
    return render_template('bootstrap_page.html')

if __name__ == '__main__':
    app.run(debug=True)