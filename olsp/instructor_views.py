from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Chat
from django.shortcuts import redirect
from itertools import chain
from datetime import date, datetime
from . import models
import datetime
from dateutil.parser import parse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import os
import re
import subprocess

def stream(request,x,y):
    name=request.GET.get('name')
    path=settings.MEDIA_ROOT+name[6:]
    chunk=[]
    if int(y)>int(x):
        with open(path, 'rb') as video_file:
            for i in range(int(x),int(y)):
                byte = video_file.read(8192)
                if not byte:
                    break
                chunk.append(byte)
            video_file.seek(int(y)*8192)
            for i in range(100):
                byte = video_file.read(8192)
                if not byte:
                    break
                chunk.append(byte)

    response=StreamingHttpResponse(chunk, content_type='application/octet-stream')
    response['Cache-Control'] = 'no-cache'
    response['Content-Type'] = 'video/mp4'
    return response

def course(request):
    use=models.User.objects.get(email=request.session['id'])
    name=models.Categories.objects.all()
    return render(request,'course.html',{'cat':name,'use':use})

def createcourse(request):
    use=models.User.objects.get(email=request.session['id'])
    date1 = parse(request.POST['crsstart'])
    date2 = parse(request.POST['crsend'])
    date3=  parse(str(datetime.datetime.now()))
    if date1>=date2:
        name=models.Categories.objects.all()
        return render(request,'course.html',{'error':'End date can not be earlier than Start date','cat':name,'use':use})
    #elif date1<date3:
        #name=models.Categories.objects.all()
        #return render(request,'course.html',{'error':'Course can not start earlier then current date.','cat':name,'use':use})
    else:
        if len(request.FILES)!=0:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            if uploaded_file_url:
                b=models.Categories.objects.get(name=request.POST['catname'])
                c=models.User.objects.get(email=request.session['id'])
                course=models.Course.objects.create(inst=c,name=request.POST['crsname'],description =request.POST['crsdescp'],
                startdate =request.POST['crsstart'],enddate=request.POST['crsend'],category =b,picture=uploaded_file_url)
                return redirect('course_detail',course.id )
        else :
            b=models.Categories.objects.get(name=request.POST['catname'])
            c=models.User.objects.get(email=request.session['id'])
            course=models.Course.objects.create(inst=c,name=request.POST['crsname'],description =request.POST['crsdescp'],
            startdate =request.POST['crsstart'],enddate=request.POST['crsend'],category =b)
            return redirect('course_detail',course.id )


def mycourse(request):
    if request.session.has_key('id'):
        user=models.User.objects.get(email=request.session['id'])
        course=models.Course.objects.filter(inst=user)
        chapter=models.Chapter.objects.all()
        return render(request,'mycourse.html',{'course':course,'chptr':chapter,'use':user,})
    else:
        return render(request,'main.html')

def addmaterial(request):
    if request.session.has_key('id'):
        use=models.User.objects.get(email=request.session['id'])
        get=request.GET.get('wut')
        return render(request,'addmaterial.html',{'idd':get,'use':use})
    else:
        return render(request,'main.html')


def addchapter(request):
    if request.session.has_key('id'):
        use=models.User.objects.get(email=request.session['id'])
        date1 = parse(request.POST['crsstart'])
        date2 = parse(request.POST['crsend'])
        c=models.Course.objects.get(id=request.POST['cid'])
        date3=  parse(str(c.startdate))
        date4=parse(str(datetime.datetime.now()))
        crsend = parse(str(c.enddate))

        if date1>=date2:
            return render(request,'addmaterial.html',{'error':'End date can not be earlier than Start date of the chapter','idd':c.id,'use':use})
        elif date1>=crsend:
            return render(request,'addmaterial.html',{'error':'Chapter can not start later then the end date of the course.','idd':c.id,'use':use})
        elif date1<=date3:
            return render(request,'addmaterial.html',{'error':'Chapter can not start earlier then the course start date.','idd':c.id,'use':use})
        else:
            models.Chapter.objects.create(course=c,name=request.POST['crsname'],startdate=request.POST['crsstart'],enddate=request.POST['crsend'])
            #return redirect("mycourse")
            return redirect('course_detail',c.id )
    else:
        return redirect('main')

def addmat(request):
    if request.session.has_key('id'):
        use=models.User.objects.get(email=request.session['id'])
        return render(request,"addchapter.html",{'chpid':request.POST['chpid'],'courseid':request.POST['courseid'],'use':use})
    else:
        return redirect('main')

def addmattochptr(request, pk):
    if request.session.has_key('id'):

        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url:
            c=models.Chapter.objects.get(id=request.POST['cpid'])
            models.Material.objects.create(chapter=c,type=request.POST['typee'],matpath=uploaded_file_url,description=request.POST['Description'])

        return redirect('course_detail',pk )
    else:
        return redirect('main')

def lecturepage(request):
    if request.session.has_key('id'):
        if request.method=='POST':
            use=models.User.objects.get(email=request.session['id'])
            crs=models.Course.objects.get(id=request.POST['courseid'])
            chptr=models.Chapter.objects.filter(course=crs)
            mtrl=models.Material.objects.filter(chapter__in=[i.id for i in chptr])

            users=models.TakenCourse.objects.filter(course=crs)
            return render(request,"lecturepage.html",{'mtrl':mtrl,'chptr':chptr,'crs':crs,'users':users,'use':use})
        return render(request,"lecturepage.html",{'use':use})
    else:
        return redirect('main')

def deletechapter(request, pk):
    if request.session.has_key('id'):
         models.Chapter.objects.get(id=request.POST['chptrid']).delete()
         return redirect('course_detail',pk )
    else:
        return redirect('main')
def deletecourse(request):
    if request.session.has_key('id'):
         models.Course.objects.get(id=request.POST['courseid']).delete()
         return redirect("main")
    else:
        return redirect('main')

def modifymat(request,pk,pk1):
    if request.session.has_key('id'):
        use=models.User.objects.get(email=request.session['id'])
        crs=models.Course.objects.get(id=pk)
        chptr=models.Chapter.objects.filter(course=crs)
        mtrl=models.Material.objects.get(id=pk1)
        return render(request,"modifymat.html",{'i':mtrl,'chptrr':pk1,'crs':crs,'use':use})
    else:
        return redirect('main')

def modifychapter(request):
    if request.session.has_key('id'):
        use=models.User.objects.get(email=request.session['id'])
        chptr=models.Chapter.objects.get(id=request.POST['chptrid'])
        return render(request,"modifychapter.html",{'chptr':chptr,'use':use})
    else:
        return redirect('main')
def modifychptr(request):
    if request.session.has_key('id'):
        chptr=models.Chapter.objects.get(id=request.POST['cid'])
        chptr.name=request.POST['crsname']
        chptr.startdate=request.POST['crsstart']
        chptr.enddate=request.POST['crsend']
        chptr.save()

        return redirect("mycourse")
    else:
        return redirect('main')
def updatematerial(request,pk):
    if request.session.has_key('id'):

        if len(request.FILES)!=0:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            size = 0
            if request.POST['typee'] == "PICTURE":
                size = 5000000
            elif request.POST['typee'] == "PDF":
                size = 5000000
            elif request.POST['typee'] == "VIDEO":
                size = 500000000
            elif request.POST['typee'] == "TEXT":
                size = 50000
            if len(request.FILES['myfile']) < size:
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
            else:
                uploaded_file_url = 0

            if uploaded_file_url:
                mtrl=models.Material.objects.get(id=request.POST['mtrlid'])
                mtrl.matpath=uploaded_file_url

                mtrl.description=request.POST['Description']
                mtrl.type=request.POST['typee']
                mtrl.save()
            else:
                mtrl=models.Material.objects.get(id=request.POST['mtrlid'])
                mtrl.description=request.POST['Description']
                mtrl.type=request.POST['typee']
                mtrl.save()

        return redirect('chapter_detail',mtrl.chapter.id)
    else:
        return redirect('main')

def deletematerial(request,pk):
    if request.session.has_key('id'):
        a=models.Material.objects.get(id=pk)
        b=a.chapter.id
        a.delete()

        return redirect('chapter_detail',b )
    else:
        return redirect('main')

def editdetail(request,pk):
    if request.session.has_key('id'):
        c=models.Course.objects.get(id=pk)
        if request.method=='POST':
            date1 = parse(request.POST['tarih'])
            c.description=request.POST['desc']
            c.enddate=date1
            if len(request.FILES)!=0:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                if uploaded_file_url:
                    c.picture = uploaded_file_url
            c.save()
            return redirect('course_detail',pk)


        use=models.User.objects.get(email=request.session['id'])
        return render(request,"editdetail.html",{'course':c,'use':use})
    else:
        return redirect('main')

def studentstatus(request,pk,pk1):
    if request.session.has_key('id'):
        use=models.User.objects.get(email=request.session['id'])
        taken = []
        nontaken = []
        course=models.Course.objects.get(id=pk)
        students=models.TakenCourse.objects.filter(course=course)
        taken1=models.Taken.objects.filter(user__in = [i.user for i in students])
        for i in taken1:
            if i.course == course:
                taken.append(i)
        for i in students:
            for j in taken:
                if i.course != j.course:
                    nontaken.append(j)
        count = 0
        chapter=models.Chapter.objects.filter(course=course)
        for i in chapter:
            material=models.Material.objects.filter(chapter=i)
            for j in material:
                count = count+1


        nottaken = models.Material.objects.filter(chapter__in=[i for i in chapter]).exclude(id__in=[i.material.id for i in taken])



        return render(request,'test2.html',{'course':course,'students':students,'taken':taken,'nottaken':nottaken,'material':count,'id':pk,'use':use})


    else:
        return redirect('main')



def assignment(request,pk):
    if request.session.has_key('id'):
        if request.method == 'POST':
            assign = models.Assignment.objects.get(aspath=request.POST['path'])
            assign.status=2
            assign.save()
            return redirect('assignment',pk)

        use=models.User.objects.get(email=request.session['id'])
        course=models.Course.objects.get(id=pk)
        takencourse=models.TakenCourse.objects.filter(course=course)
        assign = models.Assignment.objects.filter(user__in=[i.user for i in takencourse])
        return render(request,'assignment.html',{'assign':assign,'id':pk,'use':use})

    else:
        return redirect('main')


def visibility(request):
    if request.session.has_key('id'):
        chapter=models.Chapter.objects.get(id=request.POST['chid'])
        if chapter.showtoggle == 0 :
            chapter.showtoggle = 1
            chapter.save()
            return redirect('course_detail',chapter.course.id)
        else:
            chapter.showtoggle = 0
            chapter.save()
            return redirect('course_detail',chapter.course.id)
    else:
        return redirect('main')








