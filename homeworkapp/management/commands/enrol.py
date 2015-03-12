# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

import csv
from optparse import make_option
from homeworkapp.models import Course

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                    make_option('--input',
                                action='store', 
                                dest='input',
                                help='the input file'),
                    make_option('--course',
                                action='store', 
                                dest='course',
                                help='the course'))

    def handle(self, *args, **options):
        fn = options['input']
        csv_reader = csv.reader(open(fn))
        
        course = Course.objects.get(slug=options['course'])
        
        for row in csv_reader:
            sn = row[0]
            u = User.objects.get(username=sn)
            course.students.add(u)
            self.stdout.write(sn)

