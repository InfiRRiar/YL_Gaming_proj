from flask import Flask, render_template, redirect
from flask_restful import abort, Api
import news_resources
import projects_resources
import library_recources
import reports_resources
from __all_forms import LoginForm, RegistrationForm, CreateNewsForm, CreateProjectForm, ChangePasswordForm, \
    FindErrorForm
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
app.config['JSON_AS_ASCII'] = False  # чтобы в API русские символы нормально отображались
app.config['SECRET_KEY'] = '13fth14hg83g93hg13hg1b9h8b13v4n2i'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=12)  # автовыход из акканта через 12 часов


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')  # главаня страница, просто информация о сайте
def main_page():
    return render_template('main.html')


@app.route("/news/<int:id>")  # отображение определенной новости
@login_required  # ее можно посмотреть. только если пользватель вошел в аккаунт
def full_news(id):
    news = get('http://127.0.0.1:8080/api/v2/news/' + str(id)).json()['news']  # получение json одной новости
    if news:  # если нет такой новости, то...
        news['created_date'] = str(news['created_date'])[0:10]  # дата округляется с точностью до дня
        return render_template("full_news.html", news=news)
    abort(404)  # ...возвращаем ошибку 404


@app.route('/support',
           methods=["GET", "POST"])  # страница для обращения пользователя администраторам, если найдена ошибка
@login_required  # можно написать обращение, только если вошел в аккаунт
def support_page():
    form = FindErrorForm()  # форма создания репорта
    if form.validate_on_submit():  # если нажали на кнопку, то заносим в БД новый репорт
        post("http://127.0.0.1:8080/api/v2/reports", json={
            "title": form.title.data,
            "content": form.content.data,
            "author": current_user.username}
             )
        return redirect("/")  # переадресация на главную станицу
    return render_template('support.html', form=form)


@app.route("/reports")  # отображение всех репортов
@login_required
def all_reports():
    if current_user.is_developer:  # страница доступна только для администраторов
        reports = get('http://127.0.0.1:8080/api/v2/reports').json()['reports']
        for item in reports:
            item['id'] = str(item['id'])  # тоже преобразование с string для создания ссылки на html форме
        reports.reverse()  # реверс для отображения сначала новых репортов
        return render_template('reports.html', reports=reports)
    abort(403)  # ошибка: недостаточно прав


@app.route("/full_report/<int:id>")  # отображение полностью одного репорта
@login_required
def full_report(id):
    if current_user.is_developer:  # доступно только администраторам
        report = get('http://127.0.0.1:8080/api/v2/reports/' + str(id)).json()['report']  # получения json репорта
        if report:
            report["id"] = str(report["id"])  # опять преобразование в string для использование в html
            return render_template("full_report.html", report=report)
        abort(404)


@app.route("/full_report/delete_report/<int:id>",
           methods=["GET", "DELETE"])  # на этот адрес будут переадресация при нажатии на ссылку с надписью "удалить"
@login_required
def delete_report(id):
    delete('http://127.0.0.1:8080/api/v2/reports/' + str(id))  # удаление репорта
    return redirect("/reports")


@app.route('/projects')  # страница со всеми проектами (играми), которые сделала компания
def projects_page():
    projects = get('http://127.0.0.1:8080/api/v2/projects').json()['projects']  # получение json всех проектов
    added_projects = list()
    session = db_session.create_session()
    session = session.query(AddedGames.project_name).filter(AddedGames.username == current_user.username).all()
    # получение список множеств id проектов, которые добавлены в библиотеку у пользователя (пример: [(1,), (2,)])
    for i in session:
        added_projects.append(str(i[0]))  # добавляем эти id без множеств (пример [(1,), (2,)] -> [1, 2])
    for i in range(len(projects)):
        projects[i]["id"] = str(projects[i]["id"])  # опять то же самое, что было в новостях и репортах...
    return render_template('projects.html', projects=projects, added_projects=added_projects)


@app.route('/add_project_lib/<int:id>', methods=['GET', 'POST'])  # добавление проекта в библиотеку пользователя
@login_required  # можно перейти только если выполнен вход в профиль
def projects_add(id):
    post('http://127.0.0.1:8080/api/v2/library', json={
        "project_name": id,  # id игры, которую добавили
        "username": current_user.username  # логин пользователя, который добавил игру
    })
    return redirect("/projects")  # возврат на страницу со всеми проектами


@app.route('/delete_project_lib/<int:id>')  # удаление проекта из библиотеки пользователя
@login_required
def delete_project(id):
    session = db_session.create_session()
    game_id = session.query(AddedGames.id).filter(AddedGames.username == current_user.username,
                                                  AddedGames.project_name == id).first()
    # получение id проекта, который надо удалить
    delete('http://127.0.0.1:8080/api/v2/library/' + str(game_id[0]))
    return redirect('/projects')


@app.route('/profile/<string:username>')  # страница профиля
@login_required
def profile_page(username):
    # статистика доступна только для того, кому она принадлежит
    if current_user.username == username or current_user.is_developer:
        session = db_session.create_session()
        session = session.query(User).filter(User.username == username).first()
        games = get('http://127.0.0.1:8080/api/v2/library').json()[
            'games']  # получение всех игр, добавленных у всех пользователей
        user_lib = list()
        for i in games:
            if i["username"] == current_user.username:
                user_lib.append(
                    i["project_name"])  # в список добавляются те игры, которые добавлены именно у этого пользователя
        all_proj = get("http://127.0.0.1:8080/api/v2/projects").json()["projects"]  # получение всех проектов компании
        games = list()
        for i in all_proj:
            if i["id"] in user_lib:
                # если игра находится в библиотеки у пользователя, то информация о ней добавляется в переменную
                i["id"] = str(i["id"])
                games.append(i)
        return render_template('profile.html', user=session, games=games)
    abort(403)


@app.route('/login', methods=['GET', 'POST'])  # страница входа в аккаунт
def login():
    form = LoginForm()  # не был уверен, что по API уместно передававть пароль, поэтому сделал по старому
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):  # если есть такой пользователей есть и пароль такой же,
            login_user(user)  # то вход в аккаунт будет произведен
            return redirect("/")
        return render_template('login.html',  # иначе на странице появляется сообщение "неправильных логин или пароль"
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])  # регистрация
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.username == form.username.data).first():
            # если пользователь уже есть в базе данных
            return render_template('register.html', message="Такой логин существует", form=form)
        code = ""
        for i in range(8):
            code = code + str(random.randint(0, 10))  # формирование пароля для привязки аккаунта ВК
        user = User(
            username=form.username.data,  # в БД заносится логин,
            submit_code=code)  # код привязки ВК
        user.set_password(form.password.data)  # устанавливается пароль
        session.add(user)
        session.commit()
        login_user(user)
        return redirect('/confirm_vk/' + form.username.data)  # redirect на страницу с инструкцией по привязке ВК
    return render_template("register.html", form=form)


@app.route('/confirm_vk/<string:name>')  # страница с инструкцией по привзяке вк
@login_required
def confirm(name):
    session = db_session.create_session()
    user = session.query(User.submit_code).filter(User.username == name)
    # получение кода этого пользователя для привязки ВК
    return render_template('confirm.html', code=user[0][0])


@app.route('/create')  # страница с выбором, что добавить на сайт - проект или новость
@login_required
def create():  # в ней только HTML и CSS
    if current_user.is_developer:  # доступно только администраторам
        return render_template("create.html")
    abort(403)  # ошибка: недостаточно прав


@app.route("/create_news", methods=['GET', 'POST'])  # создание новости
@login_required
def create_news():
    if current_user.is_developer:  # только администраторы
        form = CreateNewsForm()
        if form.validate_on_submit():
            post("http://127.0.0.1:8080/api/v2/news", json={  # занесение данных новости
                'title': form.title.data,
                'content': form.content.data,
                'author': form.author.data})
            return redirect("/create")
        return render_template("create_news.html", form=form)
    abort(403)  # ошибка: недостаточно прав


@app.route("/create_project", methods=['GET', 'POST'])  # добавление проекта
@login_required
def create_project():
    if current_user.is_developer:  # только администраторы
        form = CreateProjectForm()
        if form.validate_on_submit():
            post("http://127.0.0.1:8080/api/v2/projects", json={  # добавление проекта
                'title': form.title.data,
                'content': form.content.data,
                'download_link': form.download_link.data  # ссылка на скачивание игры
            })
            return redirect("/create")
        return render_template("create_project.html", form=form)
    abort(403)


@app.route('/change_password', methods=['GET', 'POST'])  # изменение пароля
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(current_user.id == User.id).first()
        # получение информации о текущем пользователе
        if not user.check_password(form.exist_password.data):  # если не пройдена проверка старого пароля на подлинность
            return render_template("change_password.html", form=form, message="Старый пароль указан неверно")
        if form.new_password.data != form.repeat_password.data:  # если новый пароль, введенный в 2ух input не свопадает
            return render_template("change_password.html", form=form, message="Пароли не совпадают")
        user.set_password(form.new_password.data)  # если все ОК, устанавливается новый пароль
        session.add(user)
        session.commit()
        return redirect("/profile/" + str(current_user.username))  # редирект на странцу профиля
    return render_template("change_password.html", form=form)


@app.route('/logout')  # просто выход из аккаунта
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/change_vk')  # привязка к профилю другой ВК
@login_required
def change_vk():
    session = db_session.create_session()
    user = session.query(User).filter(
        User.username == current_user.username).first()  # информация о текущем пользователе
    user.is_submit = 0  # изменение подтверждение профиля на False (профиль ВК теперь не подтвержден)
    code = ""
    for i in range(8):
        code = code + str(random.randint(0, 9))  # генерация кода подтверждения
    user.submit_code = code
    session.add(user)
    session.commit()
    return render_template('confirm.html', code=code)  # HTML файл с инструкцией по подтвержению профиля ВК


@app.errorhandler(403)  # оформление ошибки 403
def page_not_found(e):
    return render_template('error403.html')  # так она будет выглядеть


def main():
    # API новостей
    api.add_resource(news_resources.NewsListResource, '/api/v2/news')
    api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
    # API проектов
    api.add_resource(projects_resources.ProjectsListResource, '/api/v2/projects')
    api.add_resource(projects_resources.ProjectsResource, '/api/v2/projects/<int:projects_id>')
    # API библиотек пользователей
    api.add_resource(library_recources.AddedGamesListResource, '/api/v2/library')
    api.add_resource(library_recources.AddedGamesResource, '/api/v2/library/<int:game_id>')
    # API репортов
    api.add_resource(reports_resources.ReportsListResource, '/api/v2/reports')
    api.add_resource(reports_resources.ReportsResource, '/api/v2/reports/<int:report_id>')

    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
