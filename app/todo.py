"""
Blueprint with todo views
"""
from flask import Blueprint, render_template, request, redirect, url_for,session
from bson.objectid import ObjectId
from flask.views import MethodView
from forms import CreateTodoForm
from model import Todo, User
from flask.ext.login import login_required, current_user

todo = Blueprint('todo', __name__, template_folder='templates')

get_dict = lambda dct, *keys: {key:dct[key] for key in keys}

class SearchView(MethodView):
    @login_required
    def get(self, condition):
        try:
            todos = Todo.objects(topic__contains=condition)
        except:
            return redirect(url_for('todo.list', error='Search Fail!'))
        return render_template('todo/search_result.html', todos=todos)

class DeleteView(MethodView):
    '''
    Delete todo.
    '''
    def get(self, obj_id):
        try:
            Todo.objects(id=obj_id).delete()
        except:
            redirect(url_for('todo.list', message=u'Delete Fail!!!'))
        return redirect(url_for('todo.list'))

class CreateView(MethodView):
    """
    Create todo.

    get:Create Form
    post:check infomation and write into the MongoDB
    """
    @login_required
    def get(self):
        form = CreateTodoForm()
        return render_template('todo/create.html',
                form = form)

    def post(self):
        form = CreateTodoForm()
        if form.validate_on_submit():
            data = get_dict(request.form, 'topic', 'start', 'end', 'desc')
            todo = Todo(**data)
            todo.poster = ObjectId(session["user_id"])
            try:
                todo.save()
            except:
                return redirect(url_for('todo.create'))
        return redirect(url_for('todo.list'))

class ListView(MethodView):
    """
    List view.
    """
    @login_required
    def get(self):
        return render_template('todo/list.html',
            todos = Todo.objects(done=None, poster=ObjectId(session["user_id"])).order_by('end'),
            dones=Todo.objects(done=True, poster=ObjectId(session["user_id"])).order_by('end'))

class NoteView(MethodView):
    '''
    Create a Note or Question with a todo.
   '''
    @login_required
    def get(self, obj_id):
        pass

class UpdateView(MethodView):
    '''
    Modify a todo

    get : show the update form and todo infomation
    post : update the infomation in the MongoDB,
        front-end should preare the data
        bake-end should insert into Database.
    '''
    @login_required
    def get(self, obj_id):

        form = CreateTodoForm()
        todo = Todo.objects.with_id(obj_id)
        return render_template('todo/update.html',
                todo=todo,
                form=form)

    @login_required
    def post(self, obj_id):

        try:
            todo = Todo.objects.with_id(obj_id)
        except:
            return redirect(url_for('todo.list', error=u"DB didn't have this infomation."))
        if todo.poster is None:
            todo.poster = ObjectId(session["user_id"])
        update = get_dict(request.form, 'topic', 'start', 'end', 'desc')
        for key in update:
            if update[key]!='':
                todo[key] = update[key]
        todo.save()
        return redirect(url_for('todo.list'))

class DoneView(MethodView):
    '''
    Finish a job then we will close this one.
    '''
    @login_required
    def get(self, obj_id):
        try:
            todo = Todo.objects.with_id(obj_id)
        except:
            return redirect(url_for('todo.list', error=u"DB didn't have this infomation."))
        todo.done = True
        try:
            todo.save()
        except:
            print 'fail'
        return redirect(url_for('todo.list'))

todo.add_url_rule('/QASystem/create/todo/', view_func = CreateView.as_view('create'))
todo.add_url_rule('/QASystem/list/', view_func = ListView.as_view('list'))
todo.add_url_rule('/QASystem/del/<obj_id>/', view_func = DeleteView.as_view('delete'))
todo.add_url_rule('/QASystem/update/<obj_id>/', view_func = UpdateView.as_view('update'))
todo.add_url_rule('/QASystem/note/<obj_id>/', view_func = NoteView.as_view('note'))
todo.add_url_rule('/QASystem/done/<obj_id>/', view_func=DoneView.as_view('done'))
todo.add_url_rule('/QASystem/search/<condition>/', view_func=SearchView.as_view('search'))
