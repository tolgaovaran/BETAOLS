
# Create your views here.

def index(request):
    return render(request,"index.html")

def panel(request):
        return render(request,"index.html")

from django.contrib.sessions.models import Session
from django.http import HttpResponse , JsonResponse
from .models import User, Chat, CourseChat , Course ,TakenCourse ,Categories
from django.shortcuts import redirect ,get_object_or_404 ,render
from itertools import chain
from datetime import date, datetime
from django.utils import timezone
from django.core import serializers


#TEST IS Here
def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []

    for session in active_sessions:
        data = session.get_decoded()
       # if data.get('id', None) not in user_id_list :
       #     user_id_list.append(data.get('id', None))
        user_id_list.append(data.get('id', None))
    # Query all logged in users based on id list
    #return User.objects.filter(email=user_id_list)
    return user_id_list


def logout_forreal(user):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    make_off(user)
    for session in active_sessions:
        data = session.get_decoded()
        if data.get('id', None) == user.email :
            session.delete()

    return True


def test3(request):
    tk=list()
    tv=list()
    t=list()
    for key, value in request.session.items():
        tk.append(key)
        tv.append(value)
        print('{} => {}'.format(key, value))
    t=get_current_users()
    tt={'tk':tk,
        'tv':tv,
        'online':t,
        'onl':z}
#    for s in Session.objects.filter():
#      s.delete()
    return render(request,'n/test.html',tt)

def chatbygroup(sender_,user):
    cc=CourseChat.objects.filter(course=sender_).exclude(sender=user)
    gchat=list(CourseChat.objects.filter(course=sender_).exclude(sender=user).values('seen'))
    cont={'group':sender_,
          'gchat':gchat,
            }
    return cont

def chatbyuser(sender_,user):

    chats = list( Chat.objects.filter(seen=0,receiver=user,sender=sender_).values('seen'))
    cont={'id':sender_,
          'chats':chats,
            }
    return cont



def senderfinder(use):
    sender=list()
    chats=Chat.objects.filter(seen=0,receiver=use)
    for i in chats:
        if i.sender.id not in sender :
            sender.append(i.sender.id)
    return sender

def test2(request):
    catagory=list(Categories.objects.all().values('name','id'))
    users = list( User.objects.all().values('id', 'name','status','email','surname'))
    alluser=User.objects.all()
    everything=list()
    for j in alluser:

        chats=list()
        gchat=list()


        senderz=senderfinder(j)
        groups=enrolled_courses(j)

        for i in groups:
            gchat.append(chatbygroup(i,j))

        for i in senderz:
            chats.append(chatbyuser(i,j))
        chats={'chat':chats,'gchat':gchat}
        infoforuser={'name':j.name,'id':j.id,'surname':j.surname,'chats':chats,}
        everything.append(infoforuser)


    return JsonResponse({'Users':users,'everything':everything,'Cate':catagory,})

  #  return JsonResponse({'musers':muser,'Users':users,'chat':chats,'gchat':gchat,'Cate':catagory,})


def test11(request):

    user=User.objects.all()

    unsee=unseen_msg(user)

    cont={'use':user,
           'unsee':unsee }
    return render(request,"n/test.html",cont)

def test(request):
    us=User.objects.get(email=request.session['id'])
    user=User.objects.all()


    tt=list()
    chats = Chat.objects.filter(seen=0,receiver=us)#order_by('sender').distinct()
    for i in chats:
        tt.append(chatbyuser(i.sender,us))



    use=User.objects.get(email=request.session['id'])
    user=User.objects.all()

    unsee=unseen_msg(use)
    cont={'use':user,
            'tt':tt,
           'unsee':unsee }
    return render(request,"n/test.html",cont)

def chat(request):
    u1=User.objects.get(email=request.session['id'])
    typ=request.GET.get('msjto')[0]
    target=request.GET.get('msjto')[1:]

    chat =get_messages(u1,typ,target)
    if typ=='g':
        count={'count':msgcounter(target),}
        chat.update(count)
    return render(request, 'n/testbase.html',chat)


def post(request):
    user1=User.objects.get(email=request.session['id'])

    if request.method == "POST":
        reci=request.POST.get('target', None)
        msg=request.POST.get('msgbox', None)
        typ=request.POST.get('type', None)

        if typ=='u':
            user2=User.objects.get(email=reci)
            cht=Chat()
            cht.sender= user1
            cht.receiver =user2
            cht.message =msg
            cht.date = datetime.now()
            cht.seen = '0'
            if len(msg)>0:
                cht.save()
            return JsonResponse({ 'msg': msg, 'un':user1.name ,'usn':user1.surname,'receiver':user2.email })

        if typ =='g':
            cour=Course.objects.get(id=reci)
            gcht=CourseChat()
            gcht.sender = user1
            gcht.course = cour
            gcht.message =msg
            gcht.date = datetime.now()
            gcht.seen =msgcounter(cour)+1
            if len(msg)>0:
                gcht.save()
            return JsonResponse({ 'msg': msg, 'user':user1.email ,'receiver':cour.id })
    else:
        return HttpResponse('Request must be POST.')



def messages(request):
    u1=User.objects.get(email=request.session['id'])
    typ=request.GET.get('msjto')[0]
    target=request.GET.get('msjto')[1:]
    chat =get_messages(u1,typ,target)

    return render(request, 'n/testmessage.html',chat)



#  Functions are here.
def unseen_msg(use):
    unseen=list()
    chat=Chat.objects.filter(receiver=use)
    for i in chat:
        if i.seen == '0' :
            unseen.append(i)

    return unseen


# 1-1 msjlarda mesaj gonderilince seen 0 olacak diger taraf grounce 1 e cevrilcek
# gurup mesajlari ???
#
#

def msgcounter(cours):
    count=0

    chat=CourseChat.objects.all().filter(course=cours)
    for i in chat:
        count+=1
    return count

def chatmain(use):
    us=use
    ctaken=enrolled_cour(us)

    mesage=Chat.objects.all().filter(receiver=us)
    everybody=User.objects.all().exclude(email=us)

    prev=list()
    for i in mesage :
        if i.sender not in prev :
           prev.append(i.sender)

    cont= {
          'use':us,
          'everybody':everybody,
          'prev':prev,
          'coursetkn':ctaken,
                   }
    #cont.update(catagory_list())

    #cont.update(enrolled_courses(us))

    return cont



def get_messages(user,typ,receiver):

    if  typ=='g':
        reci=Course.objects.get(id=receiver)
        chat=CourseChat.objects.all().filter(course=receiver)

    if typ=='u':
        reci=User.objects.get(email=receiver)

        chat1=Chat.objects.all().filter(sender=user,receiver=reci)
        chat2=Chat.objects.all().filter(sender=reci,receiver=user)
        chat2.update(seen='1')
        chat = sorted(chain(chat1, chat2), key=lambda instance: instance.date)
    cont={'use':user,
          'reci':reci,
          'chat':chat,
          'type':typ,}
    return cont

def enrolled_cour(use):

    us=use
    enrolled=TakenCourse.objects.all().filter(user=us).distinct()
    taken=list()

    for cour in enrolled:
        taken.append(cour.course)

    return taken


def enrolled_courses(use):

    us=use
    enrolled=TakenCourse.objects.all().filter(user=us).distinct()
    taken=list()

    for cour in enrolled:
        taken.append(cour.course.id)


    return taken

def enroll_count(cours):
    count=0
    enrolment=TakenCourse.objects.filter(course=cours)
    for i in enrolment:
        count+=1
    return  count

def populer_course():
    course=list()
    popi=list()
    count=list()
    courses=Course.objects.all()

    for cour in courses:
        course.append(cour.name)
        count.append(enroll_count(cour))

    populer=sorted(zip(count, course),reverse=True)[:5]
    for element in populer:
        popi.append(element[1])

    ppp=Course.objects.filter(name=popi[0])|Course.objects.filter(name=popi[1])|Course.objects.filter(name=popi[2])|Course.objects.filter(name=popi[3])|Course.objects.filter(name=popi[4])
    cont={'popi':ppp,}

    return cont


def catagory_list():
    catagory=Categories.objects.all()
    cont={'cate':catagory,}
    return cont


def course_list():
    course=Course.objects.all()
    cont={'course':course,}
    return cont

def main_cont(id):
    use=id
    cont={'use':use}
    cont.update(course_list())
    #cont.update(chatmain(id))
    return cont

def online_list(use):
    ret=User.objects.filter(status='on')
    return ret

def kickeveryone():

    use=User.objects.all()
    for i in use :
        make_off(i)

def oneveryone():

    use=User.objects.all()
    for i in use :
        make_on(i)

def make_on(user):
    id=user
    id.status ="on"
    id.save()

def make_off(user):
    id=user
    id.status ="off"
    id.save()



#  Views are here.






def freeze(request):
    u1=User.objects.get(email=request.session['id'])
    u1.status='frozen'
    u1.save()
    del request.session['id']
    return redirect("main")

def unfreeze(request):
    em=request.GET.get('unfreeze')
    u1=User.objects.get(email=em)
    u1.status='off'
    u1.save()
    return redirect("main")

def kick(request):
    em=request.GET.get('kick')
    u1=User.objects.get(email=em)
    logout_forreal(u1)
    #u1.status='off'
    #u1.save()
    return redirect("login")

def logout(request):
    u1=User.objects.get(email=request.session['id'])
    logout_forreal(u1)
    #del request.session['id']
    return redirect("main")

def profile(request):
    u1=User.objects.get(email=request.session['id'])
    if request.method == 'POST':
        u1.name=request.POST['name']
        u1.surname=request.POST['surname']
        u1.title = request.POST['title']
        u1.origin = request.POST['origin']
        u1.gender = request.POST['gender']
        u1.profession = request.POST['proff']
        u1.phonenumber = request.POST['phone']
        u1.save()

    cont=main_cont(u1)
    cont.update(origins())
    return render(request,'n/profile.html',cont)


def mycourses(request):
    return render(request,'mycourses.html')





def register(request):
    if request.method =='POST' :
        try:
            emailf=request.POST['email']
            name=request.POST['name']
            surname=request.POST['surname']
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']

            if pass1==pass2 :
                datt=date.today()
                rpass=pass1
                if User.objects.filter(email=emailf).exists() :
                    x=1
                else :
                    usr = User(None, emailf, name, surname,
                        'Turkey','none','none','dne',datt,rpass,1,'off','none')
                    usr.save()
                    x=2
                return render(request,'n/register.html',{'x':x})
            else:
                return render(request,'n/register.html',{'x':3})
        except Exception as e:
            return render(request,'n/register.html',{'x':e})

    return render(request,'n/register.html',{'x':0})


def chatshowold(request):
    typ=request.GET.get('msjto')[0]
    reciv=request.GET.get('msjto')[1:]
    u1=User.objects.get(email=request.session['id'])
    cont=get_messages(u1,typ,reciv)


    return render(request,'chatshow.html',cont)


def chatshow1old(request):
    u1=User.objects.get(email=request.session['id'])
    if request.GET.get('msjto')[0]=='u':
        user2 =request.GET.get('msjto')[1:]
        reci=User.objects.get(email=user2)
        chat1=Chat.objects.all().filter(sender=u1,receiver=reci)
        chat2=Chat.objects.all().filter(sender=reci,receiver=u1)
        chat = sorted(chain(chat1, chat2), key=lambda instance: instance.date)

    if request.GET.get('msjto')[0]=='g':
        user2 =request.GET.get('msjto')[1:]
        reci=Course.objects.get(id=user2)
        chat=CourseChat.objects.all().filter(course=user2)


    cont={'u1':u1,
          'reci':reci,
          'chat':chat,

         }
    return render(request,'chatshow.html',cont)


def chatold(request):
    u1=User.objects.get(email=request.session['id'])
    if request.GET.get('msjto')[0]=='u':
        user2 =request.GET.get('msjto')[1:]

        u2=User.objects.get(email=user2)
        cont={'u1':u1,
              'u2':u2,
              'iff':request.GET.get('msjto')[0],}
        #cont.update(chatmain(u1))
        return render(request,'chat.html',cont)

    elif request.GET.get('msjto')[0]=='g':
        courcode = request.GET.get('msjto')[1:-4]

        cour=Course.objects.get(id=courcode)
        cont={'u1':u1,
              'cour':cour,
              'iff':request.GET.get('msjto')[0],}
        cont.update(chatmain(u1))
        return render(request,'chat.html',cont)


def chatsendold(request):
    u1=User.objects.get(email=request.session['id'])
    if request.GET.get('msjto')[0]=='u':
        user2 = request.GET.get('msjto')[1:]
        u2=User.objects.get(email=user2)

        cont={'u1':u1,
              'u2':u2,
              'iff': request.GET.get('msjto')[0],}
        #cont.update(chatmain(u1))
        if request.method =='POST' :
            msg=request.POST['message']
            dat= datetime.now()
            cht1=Chat()
            cht1.sender= u1
            cht1.receiver =u2
            cht1.message =msg
            cht1.date = dat
            cht1.seen = '0'
            if len(msg)>0:
                cht1.save()


            return render(request,'chatsend.html',cont)

        return render(request,'chatsend.html',cont)

    elif request.GET.get('msjto')[0]=='g':
        courcode = request.GET.get('msjto')[1:]
        cour=Course.objects.get(id=courcode)

        cont={'u1':u1,
              'cour':cour,
              'iff': request.GET.get('msjto')[0],}
       # cont.update(chatmain(u1))

        if request.method =='POST' :
            msg=request.POST['message']
            dat= datetime.now()
            grcht=CourseChat()
            grcht.sender = u1
            grcht.course = cour
            grcht.message =msg
            grcht.date = dat
            if len(msg)>0:
                grcht.save()


            return render(request,'chatsend.html',cont)

        return render(request,'chatsend.html',cont)
    return render(request,'chatsend.html',)



def chat1(request):

    u1=User.objects.get(email=request.session['id'])
    cont=chatmain(u1)

    return render(request,'n/chatall.html',cont)



def userlogin(request):
    c='Not Logged in'
    d='You are allready online in another mashine please log out first 333'
    if request.session.has_key('id'):
        id=User.objects.get(email=request.session['id'])
        cont=main_cont(id)
        return render(request,"n/main.html",cont)

    else:

        if request.method == 'POST':

            try:
                id = User.objects.get(email=request.POST['id'])

               # if id.status=='off':
                if id.password == request.POST['password']:

                    if id.status=='frozen':

                        return render(request,"n/login.html",{'x':4,'use':id.email})
                    if id.status=='on':
                        return render(request,"n/login.html",{'x':5,'use':id.email})
                    request.session['id'] = id.email
                    cont=main_cont(id)
                    make_on(id)
                    return render(request,"n/main.html",cont)

                    return render(request,"n/login.html",{'x':1})
                else :
                    return render(request,"n/login.html",{'x':d,})
            except Exception as e:

               return render(request,"n/login.html",{'x':2})

    return render(request, "n/login.html",{'x':c,})



def main(request):
        if request.session.has_key('id'):
            id=User.objects.get(email=request.session['id'])
            cont=main_cont(id)
            return render(request,"n/main.html",cont)
        else:
            cont=course_list()
            cont.update(catagory_list())
            return render(request,'n/main.html',cont)


def origins():
    origin =["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola",
            "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba",
            "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
            "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
            "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil",
            "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso",
            "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands",
            "Central African Republic", "Chad", "Chile", "China", "Christmas Island",
            "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo",
            "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica",
            "Cote d'Ivoire", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark",
            "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt",
            "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia",
            "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France",
            "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories",
            "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland",
            "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
            "Heard and Mc Donald Islands", "Holy See (Vatican City State)", "Honduras", "Hong Kong",
            "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland",
            "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
            "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan",
            "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya",
            "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, The Former Yugoslav Republic of", "Madagascar",
            "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius",
            "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia",
            "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
            "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue",
            "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama",
            "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal",
            "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis",
            "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
            "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)",
            "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands",
            "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname",
            "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic",
            "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau",
            "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu",
            "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "United States Minor Outlying Islands",
            "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)",
            "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"];
    cont={'origin':origin,}
    return cont
