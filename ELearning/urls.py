"""ELearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views, user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('base/', views.Base, name='base'),

    path('', views.HOME, name='home'),
    
    path('course/', views.SINGLE_COURSE, name='single_course'),

    path('contact/', views.CONTACT_US, name='contact_us'),

    path('about/', views.ABOUT_US, name='about_us'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/register', user_login.REGISTER, name='register'),

    path('accounts/login', user_login.DOLOGIN, name='doLogin'),

    path('product/filter-data',views.filter_data,name="filter-data"),

    path('search',views.SEARCH_COURSE,name='search_course'),

    path('course/<slug:slug>',views.COURSE_DETAILS,name='course_details'),

    path('404',views.PAGE_NOT_FOUND,name='404'),

    path('checkout/<slug:slug>',views.CHECKOUT,name='checkout'),

    path('my-course/',views.MYCOURSE,name='mycourse'),

    path('accounts/profile/',user_login.Profile,name='profile'),

    path('accounts/profile/update',user_login.Profile_Update,name='profile_update')

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
