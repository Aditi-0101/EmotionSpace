from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.main, name="main"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("tos/", views.tos, name="tos"),
    path("cg/", views.cg, name="cg"),
    path("contact/", views.contact, name="contact"),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("toggle_heart/<int:confession_id>/", views.toggle_heart, name="toggle_heart"),
    path('add_comment/<int:confession_id>/', views.add_comment, name='add_comment'),
]