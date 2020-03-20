from django import forms


class LoginForm(forms.Form):
    """ 登录表单 """
    username = forms.CharField(required=True, error_messages={"requeired": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"requeired": "请填写密码"})