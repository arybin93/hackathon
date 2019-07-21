from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.LoginFormView.as_view(), name='login'),
    path('lk/', views.lk, name='lk'),
    path('logout/', views.logout_view, name='logout'),
    path('lk/person/<int:person_id>/', views.person, name='person'),
    path('lk/person/new', views.add_person, name='new_person')
]
