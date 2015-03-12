# coding:utf-8

from django.conf.urls import patterns, url
from homeworkapp.views import (
    CreateCourseView, 
    CourseListView,
    ArchivedCourseListView,
    ArchiveCourseView,
    DeleteCourseView,
    ReviveCourseView,
    CreateAssignmentView, 
    CourseAssignmentsView,
    UpdateAssignmentView, 
    DeleteAssignmentView,
    StudentCourseListView, 
    # CreateSubmissionView,
    UploadSubmissionView,
    AssignmentDetailView,
    StuAssignmentsView, 
    SubmissionListView,
    )

from django.views.generic.base import TemplateView

urlpatterns = patterns('homeworkapp.views',
    url(r'^$', 'index', name='index'),
    # 课程管理
    url(r'^course/new$', CreateCourseView.as_view(),
        name='course-new'),

    url(r'^course/(?P<pk>\d+)/delete$',
        DeleteCourseView.as_view(), name='course-delete'),

    url(r'^course/(?P<pk>\d+)/archive$',
        ArchiveCourseView.as_view(), name='course-archive'),

    url(r'^course/(?P<pk>\d+)/revive$',
        ReviveCourseView.as_view(), name='course-revive'),

    url(r'^course/$', CourseListView.as_view(),
        name='course-list'),

    url(r'^course/archived/$', ArchivedCourseListView.as_view(),
        name='old-course-list'),

    # 作业管理...

    # 提交情况
    url(r'(?P<pk>\d+)/submissions/$',
        SubmissionListView.as_view(
        ), name='submission-list'),

    # 作业要求
    url(r'(?P<slug>[-\w]+)/assignments/new$',
        CreateAssignmentView.as_view(), name='assign-new'),
    # Listing
    url(r'(?P<slug>[-\w]+)/assignments/$',
        CourseAssignmentsView.as_view(
        ), name='assign-list'),
    # Updating
    url(r'assignments/(?P<pk>\d+)/update$',
        UpdateAssignmentView.as_view(), name='assign-edit'),
    # Deleting
    url(r'assignments/(?P<pk>\d+)/delete$',
        DeleteAssignmentView.as_view(), name='assign-del'),
    # Detail
    url(r'assignments/(?P<pk>\d+)$',
        AssignmentDetailView.as_view(
        ), name='assign-detail'),

    # Students...

    url(r'my/courses/$',
        StudentCourseListView.as_view(), name='my-courses'),

    url(r'my/(?P<slug>[-\w]+)/$',
        StuAssignmentsView.as_view(), name='my-assigns'),

    # url(r'my/(?P<course_slug>[-\w]+)/(?P<assign_id>\d+)/upload$',
    #     CreateSubmissionView.as_view(), name='my-upload'),

    url(r'my/(?P<pk>\d+)/upload$',
        UploadSubmissionView.as_view(), name='my-upload'),

    url(r'(?P<course_slug>[-\w]+)/not-in-this-class$',
        TemplateView.as_view(
            template_name='homeworkapp/not_in_class.html'),
            name='not_in_class'),
   )
