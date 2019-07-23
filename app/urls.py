from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.LoginFormView.as_view(), name='login'),
    path('lk/', views.lk, name='lk'),
    path('logout/', views.logout_view, name='logout'),
    path('lk/person/<int:person_id>/', views.person_view, name='person'),
    path('lk/person/<int:person_id>/add_doc/', views.person_add_doc, name='add_doc'),
    path('lk/person/new', views.add_person, name='new_person'),
    path('lk/ask_for_permit/', views.ask_for_permit)
]
