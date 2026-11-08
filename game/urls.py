from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index_jamp, name='index_jamp'),
    path('', views.index, name='index'),
]