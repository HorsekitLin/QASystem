from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

app.config.from_object('config')

app.wsgi_app = ProxyFix(app.wsgi_app)


app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'

db = MongoEngine(app)

get_dict = lambda dct, *keys: {key: dct[key] for key in keys}

def register_blueprints(app):
    from app.todo import todo
    from app.users import users
    from app.admin import admin
    app.register_blueprint(todo)
    app.register_blueprint(users)
    app.register_blueprint(admin)

register_blueprints(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(userid):
    return model.User.objects.with_id(userid)


from app import model
