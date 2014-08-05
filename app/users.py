"""
User Login
"""
from flask import Blueprint, render_template, redirect, url_for, request, redirect
from flask.views import MethodView
from flask.ext.login import (login_required, login_user, logout_user,
                            current_user)
from app import app
from model import User
from wtforms import ValidationError
from forms import LoginForm, EditUserForm
from os.path import join, isdir
from os import mkdir, makedirs
from werkzeug.utils import secure_filename

users  = Blueprint('users', __name__, template_folder='templates')

get_dict = lambda dct, *keys: {key:dct[key] for key in keys}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]

class CreateUserView(MethodView):
    """
    Create user view
    """
    def get(self):
        form = EditUserForm()
        return render_template("users/create.html",
                form=form)

    def post(self):
        form = EditUserForm()
        if form.validate_on_submit():
            new_user = get_dict(request.form,
                    'account',
                    'pwd',
                    'name',
                    'skills',
                    'email')

            folder = '{}/{}'.format(app.config["UPLOAD_FOLDER"], new_user["account"])
            logo = request.files['logo']
            filename = secure_filename(logo.filename)
            new_user['logo']=logo.filename
            if isdir(folder) == False:
                try:
                    makedirs(folder)
                except OSError as exc:
                    if exc.errorno == errno.EXIST and path.isdir(folder):
                        pass
                    else:
                        raise
            logo.save(join(folder, filename))
            try:
                User(**new_user).save()
            except:
                ValidationError(message='DB insert Error')
                return render_template('users/create.html',
                    form=form)
            return redirect(url_for('users.login'))
        return render_template('users/create.html', form=form)

class EditUserView(MethodView):
    """
    Edit User infomation.
    get : render Edit Form
    post : Edit user
    update :
    delete :
    """
    def get(self, uid):
        form = EditUserForm()
        user = User.objects.with_id(uid)
        return render_template('users/Edit.html',
                form=form,
                user=user)

    def post(self, uid):
        user = User.objects.with_id(uid)
        if request.files["logo"]:
            folder = '{}/{}'.format(
                    app.config["UPLOAD_FOLDER"],
                    user["account"])

            logo = request.files['logo']
            filename = secure_filename(logo.filename)
            try:
                logo.save(join(folder, filename))
            except:
                form = EditUserForm()
                ValidationError(message=u'Logo save Error!')
                return render_template('users/Edit.html',
                        form=form,
                        user=user)


            user["old_logo"].append(user["logo"])
            user["logo"] = filename

        edit_info = get_dict(request.form,
                    'pwd',
                    'name',
                    'skills',
                    'email')
        for key in edit_info:
            if edit_info[key] != '':
                user[key]=edit_info[key]

        try:
            user.save()
        except:
            form = EditUserForm()
            return render_template('users/Edit.html',
                    form=form,
                    user=user)
        return redirect(url_for("admin.info"))

class ListView(MethodView):
    def get(self):
        users = User.objects
        return render_template('users/list.html',
                users=users,
                img_path=app.config["UPLOAD_FOLDER"])

class LoginView(MethodView):
    """
    Login view.

    get: user authenticated sucess will redirect to the home page.Others will redirect to
        the login page.

    post:authenticated page
    """
    def get(self):
        if current_user.is_authenticated():
            return redirect(url_for('todo.list'))
        else:
            form = LoginForm()
            return render_template('users/login.html',form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = form._get_user()
            login_user(user)
            return redirect(url_for('todo.list'))
        return render_template('users/login.html', form=form)


class LogoutView(MethodView):
    """
    Logout view
    """
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('users.login'))


users.add_url_rule('/QASystem/', view_func=LoginView.as_view('login'))
users.add_url_rule('/QASystem/logout/', view_func=LogoutView.as_view('logout'))
users.add_url_rule('/QASystem/create/user/', view_func=CreateUserView.as_view('create'))
users.add_url_rule('/QASystem/users/list/', view_func=ListView.as_view('list'))
users.add_url_rule('/QASystem/users/edit/<uid>/', view_func=EditUserView.as_view('edit'))

