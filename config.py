from os.path import expanduser
home = expanduser("~")
UPLOAD_FOLDER = '{}/data'.format(home)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
DEBUG = True
MONGODB_SETTINGS = {"DB":"QASystem"}
CSRF_ENABLED = True
SECRET_KEY = "xup6jo3fup6"
