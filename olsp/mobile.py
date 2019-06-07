from olsp import models
from django.core import serializers
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Count

def mobile_login(request):
    queryset=""
    if request.method=='POST':

        user = models.User.objects.get(email=request.POST["email"])
        if request.POST["pass"] == user.password:
            getuser=models.User.objects.filter(email=user.email)
            queryset = serializers.serialize('json',getuser)


    return HttpResponse(queryset,content_type="application/json")

def mobile_register(request):
    queryset=""
    if request.method=='POST':
        user = models.User.objects.create(email=request.POST['email'],name=request.POST['name'],surname=request.POST['surname'],phonenumber=request.POST['phone'])
        user.password=request.POST['pass']
        user.title=request.POST['title']
        user.profession=request.POST['profession']
        user.gender=request.POST['gender']
        user.origin=request.POST['origin']

        user.save()
        getuser=models.User.objects.filter(email=user.email)
        queryset=serializers.serialize('json',getuser)
    return HttpResponse(queryset,content_type="application/json")

def mobile_usercourses(request):
    queryset="["

    if request.method=='POST':
        user = models.User.objects.get(email=request.POST["email"])

        if request.POST["pass"] == user.password:
            gettaken=models.TakenCourse.objects.filter(user=user).values("course")
            inst = models.Course.objects.filter(inst=user).values("id","name","inst","inst__name","inst__surname","description","category")
            courses=models.Course.objects.filter(id__in=[i['course'] for i in gettaken]).values("id","name","inst","inst__name","inst__surname","description","category")
            courses=courses.union(inst).distinct()

            queryset+=str(courses)[11:-2]+"]"
            return HttpResponse(queryset,content_type="application/json")

def mobile_categories(request):
    queryset=""
    categories=models.Categories.objects.all()
    queryset=serializers.serialize('json',categories)
    return HttpResponse(queryset,content_type="application/json")

def mobile_chat(request):
    #if request.method=='POST':
        queryset="["
        user=models.User.objects.get(email=request.POST["email"])
        #if request.POST["pass"]==user.password:
        chatsender=models.Chat.objects.filter(sender=user).values('receiver').distinct()
        chatreceiver=models.Chat.objects.filter(receiver=user).values('sender').distinct()
        raw1=models.User.objects.filter(id__in=[i['receiver'] for i in chatsender]).values("id","name","surname")
        raw2=models.User.objects.filter(id__in=[i['sender'] for i in chatreceiver]).values("id","name","surname")
        if raw1.count()==0 and raw2.count()>0:
            queryset+=str(raw2)[11:-2]+"]"
        elif raw2.count()>0:
            raw1=raw1.union(raw2).distinct()
        elif raw1.count()==0 and raw2.count()==0:
            queryset="[]"
        else:
            queryset+=str(raw1)[11:-2]+"]"
        return HttpResponse(queryset,content_type="application/json")

def mobile_chatdetail(request):
    if request.method=='POST':
        queryset=""
        user=models.User.objects.get(email=request.POST["email"])
        if request.POST["pass"]==user.password:
            user2=models.User.objects.get(id=request.POST["id"])
            messages1=models.Chat.objects.filter(sender=user, receiver=user2)
            messages2=models.Chat.objects.filter(sender=user2, receiver=user)
            for i in messages2:
                i.seen="1";
                i.save
            messages=messages1.union(messages2).order_by("date")
            queryset=serializers.serialize('json',messages)
    return HttpResponse(queryset,content_type="application/json")

def mobile_senddm(request):
    if request.method=='POST':
        queryset=""
        user=models.User.objects.get(email=request.POST["email"])
        if request.POST["pass"]==user.password:
            user2=models.User.objects.get(id=request.POST["id"])
            dm=models.Chat.objects.create(sender=user,receiver=user2,message=request.POST['message'],date=datetime.now(),seen="0")
            jsondm=models.Chat.objects.filter(id=dm.id)
            queryset=serializers.serialize('json',jsondm)

    return HttpResponse(queryset,content_type="application/json")

def mobile_alluser(request):
    queryset="["
    user=models.User.objects.all().values("id","name","surname")
    queryset+=str(user)[11:-2]+"]"
    return HttpResponse(queryset,content_type="application/json")

def mobile_categorycourses(request):
    queryset="[["
    category=models.Categories.objects.get(id=request.POST["category"])
    user=models.User.objects.get(id=request.POST['id'])
    taken=models.TakenCourse.objects.filter(user=user).values('course').distinct()
    owned=models.Course.objects.filter(category=category).filter(inst=user).values('id').distinct()
    cNotTaken=models.Course.objects.filter(category=category).values("id","name","inst","inst__name","inst__surname","description").exclude(id__in=[i['course'] for i in taken]).exclude(id__in=[i["id"] for i in owned])
    cTaken=models.Course.objects.filter(category=category).filter(pk__in=[i['course'] for i in taken]).values("id","name","inst","inst__name","inst__surname","description").exclude(id__in=[i["id"] for i in owned])
    cOwned=models.Course.objects.filter(category=category).filter(pk__in=[i['id'] for i in owned]).values("id","name","inst","inst__name","inst__surname","description")
    queryset+=str(cOwned)[11:-2]+"],["
    queryset+=str(cTaken)[11:-2]+"],["
    queryset+=str(cNotTaken)[11:-2]+"]]"

    return HttpResponse(queryset,content_type='application/json')

def mobile_chapters(request):
    queryset="[[";
    user=models.User.objects.get(id=request.POST['uid'])
    course=models.Course.objects.get(id=request.POST['cid'])
    allchapter=models.Chapter.objects.filter(course=course)
    taken=models.Taken.objects.filter(user=user,course=course).values()
    takench=models.Chapter.objects.filter(id__in=[i["chapter_id"] for i in taken]).values("id","course_id","name","showtoggle")
    queryset+=str(takench)[11:-2]+"],["
    queryset+=str(allchapter.exclude(id__in=[i["chapter_id"] for i in taken]).values("id","course_id","name","showtoggle"))[11:-2]+"]]"

    return HttpResponse(queryset,content_type='application/json')

def mobile_enroll(request):
    queryset='[{"status":"Fail"}]'
    now=datetime.now()

    if request.method=='POST':
        user=models.User.objects.get(id=request.POST["uid"])
        course=models.Course.objects.get(id=request.POST["cid"])
        try :
            models.TakenCourse.objects.get(course=course,user=user)
            queryset='[{"status":"Allready enrolled this course"}]'
        except:
            if course.startdate>now.date() or course.enddate<now.date():
                a="course date is "+str(course.startdate)+"/"+str(course.enddate)
                queryset="[{'status':'"+a+"'}]"
                return HttpResponse(queryset,"application/json")

            models.TakenCourse.objects.create(user=user,course=course)
            queryset='[{"status":"Enroll Succesfull"}]'
    return HttpResponse(queryset,content_type='application/json')

def mobile_userchapter(request):
    queryset="[{'error':'faill'}]"
    now=datetime.now()

    try:
        user=models.User.objects.get(id=request.POST["uid"])
        chapter=models.Chapter.objects.get(id=request.POST["chid"])
        if chapter.showtoggle==1:
            if chapter.startdate>now.date() or chapter.enddate<now.date():
                a="chapter date is "+str(chapter.startdate)+"/"+str(chapter.enddate)
                queryset="[{'error':'"+a+"'}]"
                return HttpResponse(queryset,"application/json")
            else:
                materials=models.Material.objects.filter(chapter=chapter).values()
                queryset="["+str(materials)[11:-2]+"]"
                return HttpResponse(queryset,"application/json")
        else:
            materials=models.Material.objects.filter(chapter=chapter).values()
            queryset="["+str(materials)[11:-2]+"]"
            return HttpResponse(queryset,"application/json")


    except:
        return HttpResponse(queryset,"application/json")

def mobile_material(request):
    queryset="[{'error':'faill'}]"

    user=models.User.objects.get(id=request.POST["uid"])
    material=models.Material.objects.get(id=request.POST["cid"])

    try:
        taken=models.Taken.objects.get(user=user,material=material)

    except:
        taken=models.Taken.objects.create(user=user,course=material.chapter.course,chapter=material.chapter,material=material,status=1)
        taken.save()
    queryset="[{'error':'success'}]"
    return HttpResponse(queryset,"application/json")


def mobile_updateprofile(request):
    queryset=""
    user=models.User.objects.get(id=request.POST["id"])
    user.name=request.POST["name"]
    user.surname=request.POST["surname"]
    user.phonenumber=request.POST["phone"]
    user.title=request.POST["title"]
    user.profession=request.POST["prof"]
    user.gender=request.POST["gender"]
    user.save()

    nuser=models.User.objects.filter(id=request.POST["id"])

    queryset=serializers.serialize("json",nuser)
    return HttpResponse(queryset,"application/json")

def mobile_changePassword(request):
    queryset=""
    user=models.User.objects.get(id=request.POST["id"])
    if user.password==request.POST["pass"]:
        user.password=request.POST["newpass"]
        user.save()
        queryset="[{'status':'successfull'}]"

    else:
        queryset="[{'status':'Wrong password'}]"
    return HttpResponse(queryset,"application/json")

def mobile_coursesMessages(request):
    queryset=""
    user=models.User.objects.get(id=request.POST["uid"])
    course = models.Course.objects.get(id=request.POST["cid"])
    messages=models.CourseChat.objects.filter(course=course)

    queryset=serializers.serialize('json',messages)
    return HttpResponse(queryset,"application/json")

def mobile_sendcm(request):

    queryset=""
    user=models.User.objects.get(id=request.POST["uid"])
    course = models.Course.objects.get(id=request.POST["cid"])
    cm=models.CourseChat.objects.create(sender=user,course=course,message=request.POST['message'],date=datetime.now())
    jsoncm=models.CourseChat.objects.filter(id=cm.id)
    queryset=serializers.serialize('json',jsoncm)

    return HttpResponse(queryset,content_type="application/json")

def mobile_unenroll(request):
    queryset=[{'status':'failed'}]

    user=models.User.objects.get(id=request.POST["uid"])
    course=models.Course.objects.get(id=request.POST["cid"])
    try:
        takencourse=models.TakenCourse.objects.filter(user=user).get(course=course)
        takencourse.delete()
        chapters=models.Chapter.objects.filter(course=course).values()
        takenchapter=models.Taken.objects.filter(user=user).filter(chapter__id__in=[ i["id"] for i in chapters])
        for i in takenchapter:
            i.delete()

        queryset="[{'status':'unenrolled successfully'}]"

        return HttpResponse(queryset,content_type="application/json")
    except:
         return HttpResponse(queryset,content_type="application/json")

def mobile_allchats(request):
    user=models.User.objects.get(id=1)


    CReciever =models.Chat.objects.filter(receiver=user)

    TCourse = models.TakenCourse.objects.filter(user=user).values()
    course=models.Course.objects.filter(id__in=[ i["course_id"] for i in TCourse])
    inst=models.Course.objects.filter(inst=user)
    course=course.union(inst)
    deneme=models.Course.objects.all().values('inst').annotate(total=Count('inst'))
    return HttpResponse(deneme,content_type="application/json")

def mobile_courseusers(request):
    queryset="["
    course=models.Course.objects.get(id=request.POST["cid"])
    user=models.User.objects.get(id=course.inst.id)
    alluser=models.TakenCourse.objects.filter(course=course).values("user")
    users=models.User.objects.filter(id__in=[i["user"] for i in alluser]).exclude(id=user.id).values("id","name","surname")
    queryset+=str(users)[11:-2]+"]"
    return HttpResponse(queryset,content_type="application/json")

def mobile_deleteuser(request):
    user=models.User.objects.get(id=request.POST["id"])
    user.delete()
    queryset="[{'status':'Your account is deleted'}]"
    return HttpResponse(queryset,content_type="application/json")