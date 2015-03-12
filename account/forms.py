# -*- coding: utf-8 -*-

from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from registration.forms import RegistrationFormUniqueEmail
from .models import UserProfile


class UserRegForm(RegistrationFormUniqueEmail):
    real_name = forms.CharField(label=u'真实姓名')
    institution = forms.CharField(label=u'单位')
    interest = forms.CharField(label=u'研究方向')
    captcha = CaptchaField(label=u'验证码')
    
class PasswordFormBase(forms.Form):
    def clean(self):
        ret = super(PasswordFormBase, self).clean()
        password = ret.get('password')
        password_confirm = ret.get('password_confirm')
        
        if password and password_confirm and \
            (password != password_confirm):
            if self._errors.has_key('password_confirm'):
                self._errors['password_confirm'].append(u'两次输入的密码不同。')
            else:
                self._errors['password_confirm'] = \
                    self.error_class([u'两次输入的密码不同。', ])
        return ret


class ChangePasswordForm(PasswordFormBase):
    password_old = forms.CharField(label=u"旧密码", 
                                   min_length=6, max_length=12, 
                                   widget = forms.PasswordInput)
    
    password = forms.CharField(label=u"密码", min_length=6, max_length=12, 
                               widget = forms.PasswordInput)
                               
    password_confirm = forms.CharField(label=u"密码确认", 
                                       widget = forms.PasswordInput, 
                                       min_length=6)
    
    def clean(self):
        ret = super(ChangePasswordForm, self).clean()
        
        password = ret.get('password')
        password_old = ret.get('password_old')
        
        if password and password_old and \
            (password == password_old):
                raise ValidationError(u"新旧密码不能一致。")
        
        if password_old:
            user = authenticate(username=self.username, password=password_old)
            if not user:
                raise ValidationError(u"旧密码错。")
        
        return ret

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile

class UserProfileWithEmailUpdateForm(UserProfileUpdateForm):
    user_email = forms.EmailField()
