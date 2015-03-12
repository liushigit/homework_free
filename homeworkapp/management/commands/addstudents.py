# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
import csv
from optparse import make_option

from account.models import UserProfile

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                make_option('--input',
                    action='store', 
                    dest='input',
                    help='the input file'),
                )

    def handle(self, *args, **options):
        fn = options['input']
        csv_reader = csv.reader(open(fn))
        group = Group.objects.get(name='students')
        
        for row in csv_reader:
            sn = row[0]
            name = row[1]
            try: 
                u = User.objects.create_user(sn, '', sn)
                u.groups.add(group)
                profile = UserProfile(real_name=name, student_number=sn, user=u)
                profile.save()
            except IntegrityError:
                pass
            self.stdout.write(name.decode('utf-8').encode('cp936'))
            
    
