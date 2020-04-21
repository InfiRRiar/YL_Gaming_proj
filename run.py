from flask import Flask, url_for, request, render_template, json, redirect
from HTML_classes import LoginForm, RegistrationForm
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/news')
def news_page():
    return render_template('news.html')


@app.route('/projects')
def projects_page():
    return render_template('projects.html')


@app.route('/feedback')
def feedback_page():
    return render_template('task.html')


@app.route('/profile')
def profile_page():
    return render_template('task.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('registr.html', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')
