
from flask import Flask, render_template, request, flash
from db import Database
from func import check_file, call_tg
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="lesson_templates")
app.debug = True
db = Database("db.db")

app.config['SECRET_KEY'] = 'dshcvbjrtyuifd6543mjklh5697fne'

@app.route("/")
def index():
    return render_template('pages/index.html')

@app.route("/about")
def about():
    return render_template('pages/about.html')

@app.route("/projects")
def projects():
    all_projects = db.select_projects() #Получение всех проектов из базы данных
    print(all_projects)
    return render_template('pages/projects.html', projects=all_projects)

@app.route("/admin/add-project", methods=["GET", "POST"])
def adm_add_project():
    if request.method == "POST":
        for key in request.form:
            if request.form[key] == '':
                flash(['Не все поля заполнены!', 'red'])
                return render_template('admin/add_project.html')
        if 'file' not in request.files:
            flash(['Невозможно прочитать файл', 'red'])
            return render_template('admin/add_project.html')
        file = request.files['file']
        if file.filename == '':
            flash(['Не выбран файл', 'red'])
            return render_template('admin/add_project.html')
        if file and check_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f'static/images/{filename}')
        db.insert_projects(request.form['title'], request.form['description'], filename)
        flash(['Project added successfully', 'green'])
        return render_template('admin/add_project.html')
    return render_template('admin/add_project.html')

@app.route("/admin/del-project", methods=["GET", "POST"])
def adm_del_project():
    if request.method == 'POST':
        if request.form and 'id' in request.form:
            db.delete_project(request.form["id"])
            flash(['Project delete successfully', 'green'])
    return render_template('admin/del_project.html', projects=db.select_projects())

@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        for key in request.form:
            if request.form[key] == "":
                flash(['Не все поля заполнены', 'red'])
        flash(['Успешно! Отзыв добавлен.', 'green'])
        db.insert_reviews(request.form["author"], request.form["text"], request.form["email"])
    return render_template('pages/reviews.html', reviews=db.select_reviews())

@app.route("/admin/del-reviews", methods=["GET", "POST"])
def adm_del_reviews():
    if request.method == 'POST':
        if request.form and 'id' in request.form:
            db.delete_reviews(request.form["id"])
            flash(['Reviews delete successfully', 'green'])
    return render_template('admin/del_reviews.html', reviews=db.select_reviews())

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        for key in request.form:
            if request.form[key] == "":
                flash(['Не все поля заполнены', 'red'])
                return render_template('pages/contacts.html')
        flash(['Успешно! Ваш запрос отправлен.', 'green'])
        name = request.form['name']
        question = request.form['question']
        email = request.form['email']
        phone = request.form['phone']
        text = f'Вам уведомление✅✅✅\nОт {name}\nТелефон: {phone}\nПочта {email}\n\n{question}'
        call_tg(text)
    return render_template('pages/contacts.html')

if __name__ == '__main__':
    app.run()
