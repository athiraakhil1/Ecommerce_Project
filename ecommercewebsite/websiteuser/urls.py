from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from website import views
from websiteuser import views
from django.conf.urls.static import static
from rest_framework.authtoken.views  import obtain_auth_token
from websiteuser import apiviews

urlpatterns = [
    
    path("firstpage",views.home_page,name="firstpage"),
    path("add_register",views.user_register,name="add_register"),
    path("loginuser",views.user_login,name="loginuser"),
    path("add",apiviews.adduser,name="add"),
    path("log",apiviews.apilogin,name="log"),
    path("logout",views.logout_user,name="logout")
]









if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
