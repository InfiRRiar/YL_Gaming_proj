from flask import Flask, url_for, request, render_template, json, redirect, session
from flask_restful import reqparse, abort, Api, Resource
import news_resources
import projects_resources
import profile_resources
from __all_forms import LoginForm, RegistrationForm, CreateNewsForm, CreateProjectForm, ChangePasswordForm
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from data.added_games import AddedGames
from requests import get, delete, post
import datetime
import random

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = '13fth14hg83g93hg13hg1b9h8b13v4n2i'
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
    news = get('http://127.0.0.1:8080/api/v2/news').json()['news']
    for item in news:
        item['id'] = str(item['id'])
        item['content'] = item['content'][:195] + "..."
    news.reverse()
    return render_template('news.html', news=news)


@app.route("/news/<int:id>")
@login_required
def full_news(id):
    news = get('http://127.0.0.1:8080/api/v2/news/' + str(id)).json()['news']
    if news:
        news['created_date'] = str(news['created_date'])[0:10]
        return render_template("full_news.html", news=news)
    abort(404)


@app.route('/projects')
def projects_page():
    projects = get('http://127.0.0.1:8080/api/v2/projects').json()['projects']
    added_projects = list()
    session1 = db_session.create_session()
    session1 = session1.query(AddedGames.project_name).filter(AddedGames.username == current_user.username).all()
    for i in session1:
        added_projects.append(str(i[0]))
    for i in range(len(projects)):
        projects[i]["id"] = str(projects[i]["id"])
    return render_template('projects.html', projects=projects, added_projects=added_projects)


@app.route('/add_project/<int:id>')
def projects_add(id):
    session = db_session.create_session()
    if session.query(AddedGames).filter(AddedGames.username == current_user.username, AddedGames.project_name == id).first():
        return redirect("/projects")
    game = AddedGames(
        project_name=id,
        username=current_user.username
    )
    session.add(game)
    session.commit()
    return redirect("/projects")


@app.route('/support')
def feedback_page():
    return render_template('task.html')


@app.route('/profile/<string:username>')
def profile_page(username):
    if str(current_user.username) == username:
        profile = get('http://127.0.0.1:8080/api/v2/profile/' + username).json()['user']
        return render_template('profile.html', user=profile)
    abort(403)


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


@app.route('/registration', methods=['GET', 'POST'])  # API
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', message="Такой логин существует", form=form)
        code = ""
        for i in range(8):
            code = code + str(random.randint(0, 10))
        user = User(
            username=form.username.data,
            submit_code=code)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user)
        return redirect('/confirm_vk/' + form.username.data)
    return render_template("register.html", form=form)


@app.route('/confirm_vk/<string:name>')
def confirm(name):
    session = db_session.create_session()
    user = session.query(User.submit_code).filter(User.username == name)
    return render_template('confirm.html', code=user[0][0])


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
        form = CreateNewsForm()
        if form.validate_on_submit():
            post("http://127.0.0.1:8080/api/v2/news", json={
                'title': form.title.data,
                'content': form.content.data,
                'author': form.author.data})
            return redirect("/create")
        return render_template("create_news.html", form=form)
    abort(403)


@app.route("/create_project", methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.is_developer:
        form = CreateProjectForm()
        if form.validate_on_submit():
            post("http://127.0.0.1:8080/api/v2/projects", json={
                'title': form.title.data,
                'content': form.content.data,
                'download_link': form.download_link.data
            })
            return redirect("/create")
        return render_template("create_project.html", form=form)
    abort(403)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(current_user.id == User.id).first()
        if not user.check_password(form.exist_password.data):
            return render_template("change_password.html", form=form, message="Старый пароль указан неверно")
        if form.new_password.data != form.repeat_password.data:
            return render_template("change_password.html", form=form, message="Пароли не совпадают")
        user.set_password(form.new_password.data)
        session.add(user)
        session.commit()
        return redirect("/profile/" + str(current_user.username))
    return render_template("change_password.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/change_vk')
def change_vk():
    session = db_session.create_session()
    user = session.query(User).filter(User.username == current_user.username).first()
    user.is_submit = 0
    code = ""
    for i in range(8):
        code = code + str(random.randint(0, 9))
    user.submit_code = code
    session.add(user)
    session.commit()
    return render_template('confirm.html', code=code)


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error403.html')


def main():
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')

    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')

    api.add_resource(projects_resources.ProjectsListResource, '/api/v2/projects')

    # api.add_resource(projects_resources.ProjectsResource, '/api/v2/projects/<int:proj_id>')

    # api.add_resource(profile_resources.UserListResource, '/api/v2/profile')

    api.add_resource(profile_resources.UserResource, '/api/v2/profile/<string:username>')

    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
