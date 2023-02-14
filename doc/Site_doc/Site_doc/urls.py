"""Site_doc URL Configuration

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
from django.urls import path
from allo_doc import views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('rdv/', views.rdv, name='rdv'),
    path('rdv_ok/', views.rdv_ok, name='rdv_ok'),
    path('planning/', views.planning , name='planning'),
    path('note/', views.note_view, name='note'),
    path('note/confirm/', views.note_confirm_view, name='note_confirm'),
    path('note/liste/', views.liste_notes, name='liste_notes'),
    # path('note/<int:appointment_id>/', views.note, name='note')


    
]
