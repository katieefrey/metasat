from django.urls import path#, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<crosswalk>', views.crosswalk, name='crosswalk'),
    #re_path(r'^(?P<crosswalk>[\w\ ]+)/$', views.crosswalk, name='crosswalk'), 
    #(?P<name>[\w\ ]+)
]