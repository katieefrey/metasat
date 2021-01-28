from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='mainindex'),
    path('about', views.about, name='about'),
    path("resources", views.resources, name="resources"),
    path("resources/basic-topics", views.basics, name="basics"),
    path("resources/advanced", views.advanced, name="advanced"),
    path("resources/linked-data", views.linkeddata, name="linked-data"),
    path("resources/url-semantic-web", views.semantic, name="url-semantic-web"),
    path('contact', views.contact, name='contact'),

    #account related
    path("login", views.login_form, name="login_form"),
    path("login_view", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("account", views.account, name="account"),
    # path("register", views.register, name="register"),
    # path("registering", views.registering, name="registering"),

    #path('accounts/', include('django.contrib.auth.urls')),
]