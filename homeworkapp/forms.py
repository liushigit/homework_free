# coding=utf-8
from django import forms
from django.forms import widgets
from .models import Course, Assignment, Attachment
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

class ArchiveCourseForm(forms.Form):
    course_id = forms.IntegerField(required=True, widget=widgets.HiddenInput)

    def clean_course_id(self):
    	print self.cleaned_data['course_id']
        try:
            self.course = Course.objects.get(
                pk=self.cleaned_data['course_id'])

        except:
            raise ValidationError("No such course")

AssignmAttachInlineFormSet = inlineformset_factory(Assignment, Attachment)