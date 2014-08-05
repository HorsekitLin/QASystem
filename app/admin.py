"""
Blueprint of the Admin View
"""
from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.views import MethodView
from model import User

admin = Blueprint('admin', __name__, template_folder='templates')

class AdminView(MethodView):
    """
    Admin control view
    """
    def get(self):
        return render_template('admin/index.html',
                user=User.objects.with_id(session["user_id"]))

    def post(self):
        user = User.objects.with_id(session["user_id"])
        demourl = request.form["demo_url"]
        if demourl in user["demourl"]:
            error_msg = u'This URL already in demo url!!'
            return render_template('admin/index.html',
                user=user,
                error_msg=error_msg)
        user["demourl"].append(request.form["demo_url"])
        user.save()
        return redirect(url_for('admin.info'))

admin.add_url_rule('/QASystem/admin/', view_func=AdminView.as_view('info'))
