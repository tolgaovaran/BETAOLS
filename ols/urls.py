"""ols URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from olsp import views
from olsp import instructor_views
from olsp import course_views
from olsp import admin_views

urlpatterns = [
    url(r'^djadmin/', admin.site.urls),
    url(r'^mobile/',include('olsp.mobileurl')),
    url(r'^index$',views.index,name='index'),

    url(r'^admin/m$',admin_views.main,name='adminmain'),
    url(r'^admin/user$',admin_views.users,name='adminuser'),
    url(r'^admin/course$',admin_views.courses,name='admincourse'),
    url(r'^admin/delete$',admin_views.delete,name='admindelete'),
    url(r'^admin/freeze$',admin_views.freeze,name='adminfreeze'),
    url(r'^admin/withdraw$',admin_views.withdraw,name='adminwithdraw'),
    url(r'^admin/coursedelete$',admin_views.coursedelete,name='admincoursedelete'),
    url(r'^admin/convdelete$',admin_views.convdelete,name='adminconvdelete'),
    url(r'^admin/createcategory$',admin_views.createcategory,name='createcategory'),
    url(r'^admin/chapter$',admin_views.chapter,name='adminchapter'),
    url(r'^admin/material$',admin_views.material,name='adminmaterial'),
    url(r'^admin/chapterdelete$',admin_views.chapterdelete,name='adminchapterdelete'),
    url(r'^admin/materialdelete$',admin_views.materialdelete,name='adminmaterialdelete'),
    url(r'^admin/categorydelete$',admin_views.categorydelete,name='admincategorydelete'),
    url(r'^admin/makeonoff$',admin_views.makeonoff,name='adminmakeonoff'),
    url(r'^admin/makeonoffall$',admin_views.makeonoffall,name='adminmakeonoffall'),
    url(r'^admin/$',admin_views.adminlogin,name='adminlogin'),
    url(r'^admin/logout/$',admin_views.logout, name = 'adminlogout'),


    url(r'^p/$',views.panel,name='panel'),
    url(r'^$',views.main ,name='main'),

    url(r'^post/$',views.post, name = 'post'),
    url(r'^register/$',views.register, name = 'register'),
    url(r'^freeze/$',views.freeze, name = 'freeze'),
    url(r'^unfreeze/$',views.unfreeze, name = 'unfreeze'),
    url(r'^kick/$',views.kick, name = 'kick'),

    url(r'^logout/$',views.logout, name = 'logout'),
    url(r'^login/$',views.userlogin ,name='login'),

    url(r'^chat/$',views.chat ,name='chat'),


    url(r'^chat1/$',views.chat1 ,name='chat1'),
    url(r'^chatall/$',views.chat1 ,name='chatall'),
    url(r'^profile/$',views.profile, name ='profile'),
    url(r'^test/$',views.test, name = 'test'),
    url(r'^test3/$',views.test3, name = 'test3'),
    url(r'^test2/$',views.test2, name = 'test2'),
    url(r'^messages/$',views.messages, name = 'messages'),

    url(r'^mycourses/$',views.mycourses, name = 'mycourses'),


    url(r'^create/$',instructor_views.course, name='course'),
    url(r'^createcourse/$',instructor_views.createcourse, name='createcourse'),
    url(r'^mycourse/$',instructor_views.mycourse, name='mycourse'),
    url(r'^addmaterial/$',instructor_views.addmaterial, name='addmaterial'),
    url(r'^chapteradd/$',instructor_views.addchapter, name='addchapter'),
    url(r'^matadd/$',instructor_views.addmat, name='addmat'),
    url(r'^addmattochptr/(?P<pk>[0-9]+)/$',instructor_views.addmattochptr, name='addmattochptr'),
    url(r'^lecturepage/$',instructor_views.lecturepage, name='lecturepage'),
    url(r'^deletechapter/(?P<pk>[0-9]+)/$',instructor_views.deletechapter, name='deletechapter'),
    url(r'^editdetail/(?P<pk>[0-9]+)/$',instructor_views.editdetail, name='editdetail'),
    url(r'^deletecourse/$',instructor_views.deletecourse, name='deletecourse'),
    url(r'^modifymat/(?P<pk>[0-9]+)/(?P<pk1>[0-9]+)/$',instructor_views.modifymat, name='modifymat'),
    url(r'^modifychapter/$',instructor_views.modifychapter, name='modifychapter'),
    url(r'^modifychptr/$',instructor_views.modifychptr, name='modifychptr'),
    url(r'^updatematerial/(?P<pk>[0-9]+)/$',instructor_views.updatematerial, name='updatematerial'),
    url(r'^deletematerial/(?P<pk>[0-9]+)/$',instructor_views.deletematerial, name='deletematerial'),
    #url(r'^chapterpage/$',instructor_views.chapterpage, name='chapterpage'),
    url(r'^stream/(?P<x>(\d+))/(?P<y>(\d+))/$',instructor_views.stream, name='stream'),
    url(r'^testtt/(?P<pk>[0-9]+)/(?P<pk1>[0-9]+)/$',instructor_views.studentstatus, name='studentstatus'),
    url(r'^assignment/(?P<pk>[0-9]+)/$',instructor_views.assignment, name='assignment'),
    url(r'^visibility/$',instructor_views.visibility, name='visibility'),


    url(r'^category/$', course_views.category_list, name='category_list'),
    url(r'^category/(?P<pk>[0-9]+)/$', course_views.category_detail, name='category_detail'),
    url(r'^course/$', course_views.course_list, name='course_list'),
    url(r'^user/(?P<pk>[0-9]+)/$', course_views.inst_course_list, name='inst_course_list'),
    url(r'^course/(?P<pk>[0-9]+)/$', course_views.course_detail, name='course_detail'),
    url(r'^enroll/(?P<pk>[0-9]+)/$', course_views.enroll_course, name='enroll_course'),
    url(r'^courses/$', course_views.enroll_list, name='enroll_list'),
    url(r'^chapter/(?P<pk>[0-9]+)/$', course_views.chapter_detail, name='chapter_detail'),
    url(r'^material/(?P<pk>[0-9]+)/$', course_views.material_detail, name='material_detail'),
    url(r'^withdraw/(?P<pk>[0-9]+)/$', course_views.withdraw_course, name='withdraw_course'),
    url(r'^upload/(?P<pk>[0-9]+)/(?P<pk1>[0-9]+)/$',course_views.uploadhw, name='uploadhw'),
    url(r'^profile/$',course_views.userprofile, name='userprofile'),


]
