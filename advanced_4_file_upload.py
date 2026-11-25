import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Нужен для flash-сообщений
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем папку для загрузок, если ее нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Проверяем, есть ли файл в запросе
        if 'file' not in request.files:
            flash('Нет части с файлом')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'Файл {filename} успешно загружен!')
            return redirect(url_for('upload_file'))
        else:
            flash('Недопустимый тип файла.')
            return redirect(request.url)
            
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)