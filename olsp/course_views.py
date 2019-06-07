from django.shortcuts import render
from django.http import HttpResponse
from .models import Course, User, Chat, Categories, Chapter, Material, TakenCourse, Taken, Assignment
from django.shortcuts import redirect
from itertools import chain
from datetime import date, datetime
from . import models
from dateutil.parser import parse
from django.shortcuts import get_object_or_404
from . import views
import datetime
from django.core.files.storage import FileSystemStorage

def course_list(request):
    courses = models.Course.objects.all()
    current_user = request.session['id']
    user = models.User.objects.get(email=current_user)
    cont={'courses':courses, 'use':user}
    if User.objects.get(email=request.session['id']):
        us=User.objects.get(email=request.session['id'])
        cont.update(views.chatmain(us))
    return render(request, 'course_list.html',cont )

def course_detail(request, pk):
    if request.session.has_key('id'):
        course = get_object_or_404(Course, pk=pk)
        course_pk = pk
        current_user = request.session['id']
        chpt = models.Chapter.objects.filter(course=course)
        user = models.User.objects.get(email=current_user)
        users=models.TakenCourse.objects.filter(course=course)
        enr = models.TakenCourse.objects.filter(course=course, user=user)
        takenchp = models.Taken.objects.filter(course=course, user=user, status=1)
        status = 'ananas'
        for i in enr:
            if course == i.course and current_user == i.user.email :
                if course.inst.email != current_user:
                    status='true'
        mat=models.Material.objects.filter(chapter__in=[i for i in chpt]).exclude(id__in=[i.material.id for i in takenchp])
        mat1=models.Material.objects.filter(id__in=[i.material.id for i in takenchp])
        total = 0
        takcap = 0
        for z in chpt:
            total = total+1
        for z in takenchp:
            takcap = takcap+1
        if total != 0:
            totnum=100/total
        else:
            totnum= 0
        per = int(takcap*(totnum/2))
        currentdate = date.today()
        homeworks = models.Assignment.objects.filter(user=user)
        cont={'cors': course, 'user': current_user, 'chpt':chpt, 'mat':mat,'mat1':mat1,'status':status, 'total':totnum, 'per':per, 'users':users, 'use': user, 'taken':takenchp, 'date':currentdate, 'homeworks':homeworks}
        cont.update(views.chatmain(user))
        return render(request, 'course_detail.html', cont)
    else:
        return redirect('register')
def material_detail(request, pk):
    material = models.Material.objects.get(pk=pk)
    chid = material.chapter.id
    chapter = models.Chapter.objects.get(id=chid)
    cur_user = request.session['id']
    cid = chapter.course.id
    course = models.Course.objects.get(id=cid)
    allmat = models.Material.objects.filter(chapter=chapter)
    user = models.User.objects.get(email=cur_user)
    enroll = models.TakenCourse.objects.filter(course=chapter.course, user=user)
    status1 = 'ananasi'
    for i in enroll:
        if course == i.course and cur_user == i.user.email :
            if course.inst.email != cur_user:
                status1='true'
    takencreate = models.Taken.objects.create(course=course,user=user,chapter=chapter,status=1,material=material)
    cont={'cors': course, 'user': cur_user, 'chpt':chapter, 'mt':material,'status':status1, 'use':cur_user,'allmat':allmat}
    cont.update(views.chatmain(user))
    return render(request, 'material_detail.html',cont)

def chapter_detail(request, pk):
    chapter = models.Chapter.objects.get(pk=pk)
    cur_user = request.session['id']
    cid = chapter.course.id
    course = models.Course.objects.get(id=cid)
    user = models.User.objects.get(email=cur_user)
    enroll = models.TakenCourse.objects.filter(course=chapter.course, user=user)
    status1 = 'ananasi'
    ananas = 0
    tesla = 10
    taken=models.Taken.objects.filter(user=user,course=course)
    mater=models.Material.objects.filter(chapter=chapter).exclude(id__in=[i.material.id for i in taken])
    for i in enroll:
        if course == i.course and cur_user == i.user.email :
            if course.inst.email != cur_user:
                status1='true'

    homeworks = models.Assignment.objects.filter(user=user)
    almadiklari = models.Taken.objects.filter(user=user,course=course).exclude(material__in=[i.material for i in homeworks])
    if request.method=='POST':
        mater1=models.Material.objects.get(id = request.POST['mtrlid'])

        try:
            a=models.Taken.objects.get(material=mater1,user=user)
            ananas = request.POST['mtrlid']
        except:
            takencreate = models.Taken.objects.create(course=course,user=user,chapter=chapter,status=1,material=mater1)
            #models.Taken.objects.create(course=course,user=user,chapter=chapter,status=1,material=mater1)
            ananas = request.POST['mtrlid']
            return redirect('chapter_detail',pk)
        cont={'cors': course, 'user': cur_user, 'chpt':chapter, 'mat':mater,'status':status1, 'use':cur_user,'ananas':ananas,'taken':taken,'mater1':mater1,'homeworks':homeworks,'almadiklari':almadiklari}
        cont.update(views.chatmain(user))
        return render(request, 'chapter_detail.html',cont)
    cont={'cors': course, 'user': cur_user, 'chpt':chapter, 'mat':mater,'status':status1, 'use':cur_user,'ananas':ananas,'taken':taken,'almadiklari':almadiklari}
    cont.update(views.chatmain(user))
    return render(request, 'chapter_detail.html',cont)


def enroll_course(request, pk):
    cenroll = get_object_or_404(Course, pk=pk)
    cuser = models.User.objects.get(email = request.session['id'])
    ccreate = models.TakenCourse.objects.create(user=cuser,course=cenroll)
    cont={'cors': cenroll, 'user': cuser}
    cont.update(views.chatmain(cuser))

    #return render(request, 'enroll.html',cont )
    return redirect('course_detail',pk)

def category_list(request):
    cate = models.Categories.objects.all()
    cont={'category':cate}
    if User.objects.get(email=request.session['id']):
        us=User.objects.get(email=request.session['id'])
        cont.update(views.chatmain(us))
    return render(request, 'category_list.html',cont)

def category_detail(request, pk):
    categ = get_object_or_404(Categories, pk=pk)
    cours = models.Course.objects.all()
    cont={'categ':categ,'cours':cours}
    if User.objects.get(email=request.session['id']):
        us=User.objects.get(email=request.session['id'])
        cont.update(views.chatmain(us))
    return render(request, 'category_detail.html',cont )

def inst_course_list(request, pk):
    ins = get_object_or_404(User, pk=pk)
    current_user = request.session['id']
    user = models.User.objects.get(email=current_user)
    cou = models.Course.objects.filter(inst=ins)
    cont= {'ins':ins,'cou':cou,'use':user}
    if User.objects.get(email=request.session['id']):
        us=User.objects.get(email=request.session['id'])
        cont.update(views.chatmain(us))
    return render(request, 'inst_course_list.html',cont )

def enroll_list(request):
    current_user = request.session['id']
    user = models.User.objects.get(email=current_user)
    enr = models.TakenCourse.objects.filter(user=user)
    courses = models.Course.objects.filter(id__in=[i.course.id for i in enr])
    taken = models.Taken.objects.filter(user=user, status=1)
    chapters = models.Chapter.objects.filter(course=courses).exclude(id__in=[i.chapter.id for i in taken])
    verilen = models.Course.objects.filter(inst=user)
    materials = models.Material.objects.filter(chapter__in=[i for i in chapters]).exclude(id__in=[i.material.id for i in taken])
    homeworks = models.Assignment.objects.filter(user=user)
    cont={'user':user, 'enr':enr, 'verilen':verilen, 'use':user, 'taken':taken, 'materials':materials, 'courses':courses,'chapters':chapters,'homeworks':homeworks}
    cont.update(views.chatmain(user))
    return render(request, 'enroll_list.html', cont)

def withdraw_course(request, pk):
    cenroll = get_object_or_404(Course, pk=pk)
    cuser = models.User.objects.get(email = request.session['id'])
    chapter= models.Chapter.objects.filter(course=cenroll)
    takencreate = models.Taken.objects.filter(course=cenroll,user=cuser,chapter__in=[i for i in chapter]).delete()
    models.TakenCourse.objects.get(user=cuser,course=cenroll).delete()
    x = models.Material.objects.filter(chapter__in=[i for i in chapter])
    delete = models.Assignment.objects.filter(user=cuser,material=x).delete()
    #return render(request, 'withdraw_course.html',{{'cors':cenroll}})
    return redirect('course_detail',pk)

def uploadhw(request, pk, pk1):
    if request.session.has_key('id'):
        current_user = request.session['id']
        material = models.Material.objects.get(pk=pk)
        user = models.User.objects.get(email=current_user)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url:
            c=models.Assignment.objects.create(user=user,material=material,aspath=uploaded_file_url,date=date.today(),status=1)
        return redirect('chapter_detail',pk1)
    else:
        return redirect('mainlo')

def userprofile(request):
    if request.session.has_key('id'):
        user=models.User.objects.get(email='email')

        return render(request,'userprofile',user)
    else:
        return redirect('mainlo')
