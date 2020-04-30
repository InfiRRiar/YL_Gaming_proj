from flask import Flask, url_for, request, render_template, json, redirect, abort, session
from __all_forms import LoginForm, RegistrationForm, CreateNews, CreateProject
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from data.news import News
from data.projects import Projects
import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=12)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/news')
def news_page():
    session = db_session.create_session()
    news = session.query(News)
    news = news[::-1]
    for item in news:
        item.id = str(item.id)
    return render_template('news.html', news=news)


@app.route('/projects')
def projects_page():
    session = db_session.create_session()
    projects = session.query(Projects)
    return render_template('projects.html', projects=projects)


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
            vk_id=form.vk_id.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', form=form)


@app.route("/news/<int:id>")
@login_required
def full_news(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id).first()
    if news:
        print(1)
        return redirect("/")
    else:
        abort(404)


@app.route('/create')
@login_required
def create():
    if current_user.is_developer:
        return render_template("create.html")
    abort(403)


@app.route("/create_news", methods=['GET', 'POST'])
@login_required
def create_news():
    if current_user.is_developer:
        form = CreateNews()
        if form.validate_on_submit():
            session = db_session.create_session()
            news = News(
                title=form.title.data,
                content=request.form['content'],
                author=form.author.data
            )
            session.add(news)
            session.commit()
            return redirect("/create")
        return render_template("create_news.html", form=form)
    abort(403)


@app.route("/create_project", methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.is_developer:
        form = CreateProject()
        if form.validate_on_submit():
            session = db_session.create_session()
            project = Projects(
                title=form.title.data,
                content=request.form['content'],
                download_link=form.download_link.data
            )
            session.add(project)
            session.commit()
            return redirect("/create")
        return render_template("create_project.html", form=form)
    abort(403)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error403.html')


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
