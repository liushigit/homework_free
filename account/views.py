# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView, UpdateView
from .forms import ChangePasswordForm, UserProfileWithEmailUpdateForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
from .models import UserProfile

def captch_refresh(request):
    if request.is_ajax():
        to_json_responce = dict()
        to_json_responce['new_cptch_key'] = CaptchaStore.generate_key()
        to_json_responce['new_cptch_image'] = \
                    captcha_image_url(to_json_responce['new_cptch_key'])
        
        return HttpResponse(json.dumps(to_json_responce), 
                            content_type='application/json')

class ChangePasswordView(FormView):
    template_name = "account/change_pw.html"
    form_class = ChangePasswordForm

    success_url = reverse_lazy('account:change-pass')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        # self.request = request
        self.initial = {'username': request.user.username, }
        
        return super(ChangePasswordView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        f = super(ChangePasswordView, self).get_form(form_class)
        f.username = self.user.username
        return f
        
    def form_valid(self, form):
        self.user.set_password(form.cleaned_data['password'])
        self.user.save()
        messages.success(self.request, '密码修改成功。', 
                         extra_tags='alert alert-success')
        return super(ChangePasswordView, self).form_valid(form)
        

class ProfileUpdateView(FormView):
    template_name = 'account/update_profile.html'
    success_url = reverse_lazy('account:update-profile')
    form_class = UserProfileWithEmailUpdateForm
    
    def get_initial(self):
        return {
            'user_email': self.request.user.email, 
        }
    
    def get_form(self, form_class):
        model_class = self.get_form_class()

        if self.request.method == 'GET':
            try:
                profile = self.request.user.userprofile
            except UserProfile.DoesNotExist as e:
                profile = UserProfile()
                profile.user = self.request.user
                profile.save()

            f = model_class(initial=self.get_initial(), 
                            instance=profile)

        elif self.request.method == 'POST':
            f = model_class(self.request.POST, instance=self.request.user.userprofile)
        return f
    
    def form_valid(self, form):
        form.save()
        self.request.user.email = form.cleaned_data['user_email']
        self.request.user.save()
        return super(ProfileUpdateView, self).form_valid(form)

