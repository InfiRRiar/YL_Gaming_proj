from flask import Flask, url_for, request, render_template, json, redirect
from __all_forms import LoginForm, RegistrationForm
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required
from data.users import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


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
        session = db_session.create_session()
        user = session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # remember_me_button
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', form=form)
        user = User(
            username=form.username.data,
            discord_tag=form.discord_tag.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('http://127.0.0.1:8080/')
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')
