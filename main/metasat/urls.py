from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<element>', views.element, name='element'),
    path('term/<element>', views.element, name='element'),
]