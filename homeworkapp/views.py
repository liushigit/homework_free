# coding: utf-8
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core.files.uploadhandler import StopUpload

from django.forms.models import modelform_factory

from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import (CreateView, DeleteView,
                                       UpdateView, FormView)

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.template import RequestContext
from django.template.response import TemplateResponse

from .models import Course, Assignment, Submission
from .decorators import own_this, in_group
from .forms import ArchiveCourseForm, AssignmAttachInlineFormSet

@login_required
def index(request):
    if request.user.groups.filter(name="teachers").exists():
        return HttpResponseRedirect(reverse('homework:course-list'))
    elif request.user.groups.filter(name="students").exists():
        return HttpResponseRedirect(reverse('homework:my-courses'))


class CreateCourseView(CreateView):
    model = Course
    success_url = reverse_lazy('homework:course-list')

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCourseView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.archived = False
        form.instance.user = self.request.user
        return super(CreateCourseView, self).form_valid(form)


class ArchiveCourseView(SingleObjectMixin, View):
    model = Course
    http_method_names = ['post', 'options', 'head']

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        course.archived = True
        course.save()
        return HttpResponseRedirect(reverse('homework:course-list'))

    @own_this
    def get_object(self, queryset=None):
        return super(ArchiveCourseView, self).get_object(queryset)


class ReviveCourseView(SingleObjectMixin, View):
    model = Course
    http_method_names = ['post', 'options', 'head']

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        course.archived = False
        course.save()
        return HttpResponseRedirect(reverse('homework:course-list'))

    @own_this
    def get_object(self, queryset=None):
        return super(ReviveCourseView, self).get_object(queryset)


class DeleteCourseView(DeleteView):
    model = Course
    success_url = reverse_lazy('homework:course-list')
    http_method_names = ['post', 'options', 'head']

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteCourseView, self).dispatch(request, *args, **kwargs)

    @own_this
    def get_object(self, queryset=None):
        return super(DeleteCourseView, self).get_object(queryset)


class CourseListView(ListView):

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        print 'iswh'
        return super(CourseListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.course_set.filter(
            archived=False).annotate(n_assigns=Count('assignment'))


class ArchivedCourseListView(ListView):
    template_name = 'homeworkapp/archived_course_list.html'

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        return super(ArchivedCourseListView, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.course_set.filter(
            archived=True).annotate(n_assigns=Count('assignment'))


class StudentCourseListView(ListView):
    template_name = "homeworkapp/my_courses.html"

    @method_decorator(login_required)
    @in_group("students")
    def dispatch(self, request, *args, **kwargs):
        return super(StudentCourseListView, self)\
                    .dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.course_joined\
                    .filter(archived = False)\
                    .annotate(n_assigns = Count('assignment'))


class CourseAssignmentsView(SingleObjectMixin, ListView):
    # todo: a teacher can't view other teacher's stuff
    template_name = "homeworkapp/assignment_list.html"

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        return super(CourseAssignmentsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['course'] = self.object
        return super(CourseAssignmentsView, self).get_context_data(**kwargs)

    @own_this
    def get_object(self, queryset=None):
        return super(CourseAssignmentsView, self).get_object(queryset)

    def get_queryset(self):
        self.object = self.get_object(Course.objects.all())
        return self.object.assignment_set.values('id', 'title', 'due_date')


class StuAssignmentsView(SingleObjectMixin, ListView):
    template_name = 'homeworkapp/my_assign_list.html'

    @method_decorator(login_required)
    @in_group("students")
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object(Course.objects.all())

        if not self.object.has_student(request.user.id):
            return HttpResponseRedirect(reverse('homework:not_in_class',
                                                kwargs={
                                                    'course_slug': kwargs.get('slug'),
                                                }))
        else:
            return super(StuAssignmentsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['course'] = self.object
        return super(StuAssignmentsView, self).get_context_data(**kwargs)

    def get_queryset(self):
        s = self.object.assignment_set.all()
        flags = [i.has_user_submitted(self.request.user.id) for i in s]
        return zip(s, flags)


class CreateAssignmentView(CreateView):
    model = Assignment

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        try:
            self.course_obj = self.get_course(kwargs['slug'])
        except Course.DoesNotExist:
            raise Http404

        return super(CreateAssignmentView, self).dispatch(request, *args, **kwargs)

    @own_this
    def get_course(self, slug):
        return Course.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        kwargs['course'] = self.course_obj
        
        formset = AssignmAttachInlineFormSet()
        kwargs['formset'] = formset

        return super(CreateAssignmentView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.course = self.course_obj
        ret  = super(CreateAssignmentView, self).form_valid(form)

        formset = AssignmAttachInlineFormSet(
                    self.request.POST,
                    self.request.FILES,
                    instance = form.instance)

        if formset.is_valid():
            formset.save()
            return ret
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('homework:assign-list', 
                       kwargs={'slug': self.object.course.slug, })


class UpdateAssignmentView(UpdateView):
    model = Assignment
    template_name_suffix = '_update_form'

    @own_this
    def get_object(self, queryset=None):
        return super(UpdateAssignmentView, self).get_object(queryset)

    def get_success_url(self):
        return reverse('homework:assign-list',
                       kwargs={'slug': self.object.course.slug, })

    def get_context_data(self, **kwargs):
        formset = AssignmAttachInlineFormSet(instance=self.get_object())
        kwargs['formset'] = formset

        return super(UpdateAssignmentView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        formset = AssignmAttachInlineFormSet(
                    self.request.POST,
                    self.request.FILES,
                    instance = form.instance)
        if formset.is_valid():
            formset.save()
            return super(UpdateAssignmentView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteAssignmentView(DeleteView):
    """
    Todo: should not really delete it.
    """
    model = Assignment

    @own_this
    def get_object(self, queryset=None):
        return super(DeleteAssignmentView, self).get_object(queryset)

    def get_success_url(self):
        return reverse('homework:assign-list',
                       kwargs={'slug': self.object.course.slug, })


class UploadSubmissionView(SingleObjectMixin, FormView):
    model = Assignment

    form_class = modelform_factory(Submission)
    template_name = 'homeworkapp/submission_form.html'

    def get_success_url(self):
        return reverse('homework:my-assigns',
                       kwargs={'slug': self.object.course.slug, })

    @method_decorator(login_required)
    @in_group("students")
    def dispatch(self, request, *args, **kwargs):

        self.object = self.get_object()

        if self.object.is_due:
            raise PermissionDenied

        if not self.object.course.has_student(request.user.id):
            raise PermissionDenied

        return super(UploadSubmissionView,
                     self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        if self.request.method == 'POST':
            return self.form_class(self.request.POST,
                                   self.request.FILES)

        elif self.request.method == 'GET':
            return self.form_class()

    def form_invalid(self, form):
        return super(UploadSubmissionView, self).form_invalid(form)

    def form_valid(self, form):
        assignment = self.object

        subm = Submission.objects.filter(user = self.request.user) \
                                 .filter(assignment = assignment)

        if not subm:
            form.instance.user = self.request.user
            form.instance.assignment = assignment
            form.save()
        else:
            work = subm[0]
            work.file = form.cleaned_data['file']
            work.save()

        return super(UploadSubmissionView, self).form_valid(form)


class SubmissionListView(SingleObjectMixin, ListView):

    """allows a teacher to check the status of submissions"""
    template_name = "homeworkapp/submission_list.html"

    @method_decorator(login_required)
    @in_group("teachers")
    def dispatch(self, request, *args, **kwargs):
        return super(SubmissionListView, self).dispatch(request, *args, **kwargs)

    @own_this
    def get_object(self, queryset=None):
        return super(SubmissionListView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        c = super(SubmissionListView, self).get_context_data(**kwargs)
        c['object'] = self.object
        return c

    def get_queryset(self):
        self.object = self.get_object(Assignment.objects.all())
        return self.object.submission_set.all()


class AssignmentDetailView(DetailView):
    model = Assignment

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        if request.user.groups.filter(name="teachers").exists():
            self.user_group = "teachers"
        elif request.user.groups.filter(name="students").exists():
            self.user_group = "students"

        return super(AssignmentDetailView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.user_group == "teachers":
            return ["homeworkapp/assignment_detail.html"]
        elif self.user_group == "students":
            return ["homeworkapp/assignment_detail_stu.html"]

    def get_object(self, queryset=None):
        obj = super(AssignmentDetailView, self).get_object(queryset)

        if self.user_group == "students" and \
           (not obj.course.has_student(self.request.user.id)):
            raise PermissionDenied
        else:
            return obj
