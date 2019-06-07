from .models import User, Chat, CourseChat , Course ,TakenCourse ,Categories ,Taken , Material,Chapter ,Superuser
from django.shortcuts import redirect ,get_object_or_404 ,render
from .views import logout_forreal

def convdelete(request):
    l=list()
    l=request.GET.getlist('u')
    Chat.objects.filter(sender=l[1],receiver=l[0]).delete()
    Chat.objects.filter(sender=l[0],receiver=l[1]).delete()
    return redirect("adminmain")

def categorydelete(request):
    em=request.GET.get('ca')
    cat=Categories.objects.get(id=em)
    cat.delete()

    return redirect("adminmain")



def createcategory(request):
    ncat=Categories()
    ncat.name=request.POST['name']
    ncat.save()

    return redirect("adminmain")

def materialdelete(request):
    em=request.GET.get('m')
    ma=Material.objects.get(id=em)
    ma.delete()

    return redirect("adminmain")

def chapterdelete(request):
    em=request.GET.get('ch')
    chap=Chapter.objects.get(id=em)
    chap.delete()

    return redirect("adminmain")

def coursedelete(request):
    em=request.GET.get('c')
    cour=Course.objects.get(id=em)
    cour.delete()

    return redirect("adminmain")

def delete(request):
    em=request.GET.get('u')
    u1=User.objects.get(email=em)
    u1.delete()

    return redirect("adminmain")


def makeonoff(request):
    l=list()
    l=request.GET.getlist('u')
    us=User.objects.get(email=l[0])
    if (l[1]=='on'):
        us.status='on'
        us.save()
    elif (l[1]=='off'):
        logout_forreal(us)
    elif (l[1]=='freeze'):
        us.status='frozen'
        us.save()
    return redirect("adminmain")

def makeonoffall(request):
    em=request.GET.get('u')
    everyone=User.objects.all()
    if (em=='on'):
        for i in everyone:
            i.status='on'
            i.save()
    elif (em=='off'):
        for i in everyone:
            logout_forreal(i)

    elif (em=='freeze'):
        for i in everyone:
            i.status='frozen'
            i.save()
    return redirect("adminmain")



def freeze(request):

    em=request.GET.get('u')
    u1=User.objects.get(email=em)
    logout_forreal(u1)
    u1.status='frozen'
    u1.save()

    return redirect("adminmain")

def withdraw(request):
    l=list()
    l=request.GET.getlist('u')
    cenroll = get_object_or_404(Course, pk=l[1])
    cuser = User.objects.get(email = l[0])
    chapter= Chapter.objects.filter(course=cenroll)
    Taken.objects.filter(course=cenroll,user=cuser,chapter=chapter).delete()
    TakenCourse.objects.get(user=cuser,course=cenroll).delete()

    return redirect('adminmain')

def chats(use):
    sender=list()
    chat=Chat.objects.filter(receiver__email=use)
    for i in chat:
        if i.sender not in sender :
            sender.append(i.sender)
    return sender


def chapterfi(course):
    chapters=list()
    chap=Chapter.objects.filter(course=course)
    for i in chap:
        chapters.append(i)
    return chapters

def materialfi(chapter):
    mat=list()
    mate=Material.objects.filter(chapter=chapter)
    for i in mate:
        mat.append(i)
    return mat

def given_cour(use):
    course=Course.objects.filter(inst__email=use)
    given=list()

    for cour in course:
        given.append(cour)

    return given

def enrolled_cour(use):


    enrolled=TakenCourse.objects.all().filter(user__email=use)
    taken=list()

    for cour in enrolled:
        taken.append(cour.course)
    return taken

def enrolled_user (course):


    enrolled=TakenCourse.objects.all().filter(course=course)
    taken=list()

    for user in enrolled:
        taken.append(user)
    return taken

def mainfunc():

    cchat=CourseChat.objects.all()
    chat=Chat.objects.all()
    user=User.objects.all()
    course=Course.objects.all()
    category=Categories.objects.all()

    everything={  'user':user,
                  'chat':chat,
                  'cchat':cchat,
                  'course':course,
                  'category':category,
                  }

    return everything

def main(request):
    if request.session.has_key('id'):
        cchat=CourseChat.objects.all()
        chat=Chat.objects.all()
        user=User.objects.all()
        course=Course.objects.all()
        category=Categories.objects.all()

        everything={  'user':user,
                      'chat':chat,
                      'cchat':cchat,
                      'course':course,
                      'category':category,
                      }

        return render(request,'admin/main.html',everything)

    else:
        return render(request,"admin/alogin.html")



def users(request):
    if request.session.has_key('super'):
        use=request.GET.get('u')
        user=User.objects.get(email=use)
        if request.method == 'POST':
            user.name=request.POST['name']
            user.surname=request.POST['surname']
            user.title = request.POST['title']
            user.origin = request.POST['origin']
            user.gender = request.POST['gender']
            user.profession = request.POST['proff']
            user.phonenumber = request.POST['phone']
            user.save()


        chat=chats(use)



        enrolled=enrolled_cour(use)
        given=given_cour(use)


        everything={  'use':user,
                      'enrol':enrolled,
                      'given':given,
                        'chat':chat,
                      }

        return render(request,'admin/user.html',everything)
    else:
        return render(request,"admin/alogin.html")

def courses(request):
    if request.session.has_key('super'):
        cour=request.GET.get('c')

        course=Course.objects.get(id=cour)
        enrolled=enrolled_user(course)
        category=Categories.objects.all()
        everything={  'course':course,
                        'enrol':enrolled,
                        'category':category,
                      }
        if request.method == 'POST':

            cour=Course.objects.get(id=cour)
            cour.name=request.POST['name']
            cour.description=request.POST['description']
            cour.startdate=request.POST['startdate']
            cate=Categories.objects.get(name=request.POST['category'])
            cour.category=cate
            cour.enddate=request.POST['enddate']
            cour.save()
            enrolled=enrolled_user(course)
            category=Categories.objects.all()
            everything={  'course':course,
                        'enrol':enrolled,
                        'category':category,
                      }
            return render(request,'admin/course.html',everything)
        enrolled=enrolled_user(course)
        category=Categories.objects.all()
        chap=chapterfi(course)
        everything={  'course':course,
                        'enrol':enrolled,
                        'category':category,
                        'chap':chap,

                      }

        return render(request,'admin/course.html',everything)
    else:
        return render(request,"admin/alogin.html")


def chapter(request):
    if request.session.has_key('super'):
        chap=request.GET.get('ch')
        ch=Chapter.objects.get(id=chap)
        mat=materialfi(chap)
        if request.method == 'POST':

            ma=Chapter.objects.get(id=chap)
            ma.name=request.POST['name']
            ma.showtoggle=request.POST['showtoggle']
            ma.startdate=request.POST['startdate']
            ma.enddate=request.POST['enddate']
            ma.save()
        everything={
                    'ch':ch,
                    'mat':mat,
                      }
        return render(request,'admin/chapter.html',everything)
    else:
        return render(request,"admin/alogin.html")

def material(request):
    if request.session.has_key('super'):
        mate=request.GET.get('m')
        mat=Material.objects.get(id=mate)
        al=Material.objects.all()
        if request.method == 'POST':

            ma=Material.objects.get(id=mate)
            ma.type=request.POST['type']
            ma.description=request.POST['description']
            ma.matpath=request.POST['path']
            ma.save()
        everything={
                    'al':al,
                    'mat':mat,

                      }
        return render(request,'admin/material.html',everything)
    else:
        return render(request,"admin/alogin.html")

def logout(request):

    del request.session['super']
    return render(request,"admin/alogin.html")

def adminlogin(request):

    if request.session.has_key('super'):

        cont=mainfunc()
        return redirect('../adminlogin')

    else:

        if request.method == 'POST':

            try:

                su=request.POST['superuser']
                id = Superuser.objects.get(email=su)
                if id.password == request.POST['password']:


                    request.session['super'] = id.email
                    cont=mainfunc()
                    return render(request,"admin/main.html",cont)


                else :
                    return render(request,"admin/alogin.html",{'x':2})
            except Exception as e:

               return render(request,"admin/alogin.html",{'x':'sueeeeeeeeeeEEEEEEEEEEEEEE'})

    return render(request, "admin/alogin.html",{'x':'error',})


