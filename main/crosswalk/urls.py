from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<crosswalk>', views.crosswalk, name='crosswalk'),
]