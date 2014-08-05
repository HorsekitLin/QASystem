#-*- coding:utf-8 -*-
"""
Flask-WTF

Form componets

unresolved :  _get_user should below the model.User
"""
from flask.ext.wtf import Form
from wtforms.widgets import Input
from wtforms import (TextField, PasswordField, TextAreaField, \
        DateField, FileField, IntegerField, StringField)
from wtforms.validators import InputRequired, ValidationError, Length, Email
from model import User, Todo
#import hashlib

class EmailInput(Input):
    """
    render a email input
    """
    input_type='email'

class EmailField(StringField):
    """
    custom email field
    """
    widget=EmailInput()

class EditUserForm(Form):
    '''
    Create user form
    '''
    account = TextField(u"Account", validators=[InputRequired(message=u"Enter right account, please.")])
    pwd = TextField(u"Password", validators=[InputRequired(message=u'Password could not be empty.')])
    name = TextField(u"Nickname")
    email = EmailField(u'Email')
    skills = TextField(u'Skills')
    logo = FileField(u'Logo img')
    skills = TextField(u'Skill')

    def _get_user(self):
        try:
            user = User.objects(account=self.account.data).first()
        except MultipleObjectsReturned: #if two sections have the same name
            user = user[0]
        return user

    def validate_account(self, field):
        if self._get_user() is not None:
            raise ValidationError(u"此帳號已被註冊")


class LoginForm(Form):

    account = TextField(u"Account", validators=[InputRequired(message=u"Enter right account, please.")])
    pwd = PasswordField(u"Password",validators=[InputRequired(message=u"Enter right password, please.")])
    name = TextField(u"暱稱")

    def _get_user(self):
        try:
            user = User.objects(account=self.account.data).first()
        except MultipleObjectsReturned: #if two sections have the same name
            user = user[0]
        return user

    def validate_account(self, field):
        if self._get_user() is None:
            raise ValidationError(u"該使用者不存在")

    def validate_pwd(self, field):
        user = self._get_user()
        if user and user.pwd != field.data:
            raise ValidationError(u'密碼不正確')

class CreateTodoForm(Form):

    topic = TextField(u'Topic', validators = [InputRequired(message=u'Topic 請勿空白'),
        Length(min=1, max=100, message=u'Topic請勿超過100個字元')])
    start = DateField(u'Start', validators = [InputRequired(message=u'起始時間請勿空白')])
    end = DateField(u'End', validators = [InputRequired(message=u'結束時間請勿空白')])
    desc = TextAreaField(u'描述內容', validators = [InputRequired(message=u'描述內容請勿空白')])

