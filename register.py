from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from models import User
from flask import url_for, redirect


class UserRegisterForm(FlaskForm):
    # 定义用户名和密码是必填项
    username = StringField('账号', validators=[DataRequired()])
    phone = StringField('手机号', validators=[DataRequired(), Length])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user:
            return redirect(url_for('user.login'))
        if len(field.data) < 3:
            raise ValidationError('注册用户名不能少于3个字符')
        if len(field.data) > 20:
            raise ValidationError('注册用户名不能多于20个字符')

    def validate_password(self, field):
        if len(field.data) < 6:
            raise ValidationError('密码不能少于6个字符')
        if len(field.data) > 15:
            raise ValidationError('密码不能大于15个字符')

    def validate_password2(self, field):
        if len(field.data) < 6:
            raise ValidationError('密码不能少于6个字符')
        if len(field.data) > 15:
            raise ValidationError('密码不能大于15个字符')
