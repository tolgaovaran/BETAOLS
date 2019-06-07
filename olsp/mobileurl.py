from django.conf.urls import url
from olsp import mobile

urlpatterns = [
    url(r'^login', mobile.mobile_login,name="mobilelgn"),
    url(r'^register', mobile.mobile_register,name="mobilereg"),
    url(r'^usercourses', mobile.mobile_usercourses,name="usercourses"),
    url(r'^categories', mobile.mobile_categories,name="categories"),
    url(r'^chat', mobile.mobile_chat,name="chat"),
    url(r'^cdetail', mobile.mobile_chatdetail,name="chatdetail"),
    url(r'^senddm', mobile.mobile_senddm,name="senddm"),
    url(r'^alluser', mobile.mobile_alluser,name="alluser"),
    url(r'^categorycourses', mobile.mobile_categorycourses,name="categorycourses"),
    url(r'^chapters', mobile.mobile_chapters,name="chapters"),
    url(r'^enroll', mobile.mobile_enroll,name="enroll"),
    url(r'^userchapter', mobile.mobile_userchapter,name="userchapter"),
    url(r'^changepassword', mobile.mobile_changePassword,name="changepass"),
    url(r'^updateprofile', mobile.mobile_updateprofile,name="updateprofile"),
    url(r'^cmessages', mobile.mobile_coursesMessages,name="cMessages"),
    url(r'^sendcm', mobile.mobile_sendcm,name="sendcm"),
    url(r'^unenroll', mobile.mobile_unenroll,name="unenroll"),
    url(r'^allchats', mobile.mobile_allchats,name="allchats"),
    url(r'^courseusers', mobile.mobile_courseusers,name="courseusers"),
    url(r'^deleteuser', mobile.mobile_deleteuser,name="deleteuser"),


 ]