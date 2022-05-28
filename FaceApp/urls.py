from django.urls import path
from FaceApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
# path('',views.index,name="Index"),
path('',views.home,name="Home"),
path('opencam',views.opencam,name="opencam"),
path("register", views.register_request, name="register"),
path("login", views.login_request, name="login"),
path("logout", views.logout_request, name= "logout"),
path("addimage", views.addimage, name= "addimage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)