from django.contrib.auth.models import Group

def set_mode(request):
    try:
        g = Group.objects.get(name="teachers")
        if g in request.user.groups.all():
            is_teacher = True
        else:
            is_teacher = False
    except Group.DoesNotExist:
        is_teacher = False
    
    try:
        g_students = Group.objects.get(name="students")
        if g_students in request.user.groups.all():
            is_stu = True
        else:
            is_stu = False
    except Group.DoesNotExist:
        is_stu = False
    
    return {'is_teacher': is_teacher, 'is_student':is_stu}
