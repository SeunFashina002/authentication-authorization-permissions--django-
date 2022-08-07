from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index, name='home'),
    path('create-post/', views.create_post, name='create_post'),
    path('sign-up/', views.sign_up, name="sign_up"),
]
