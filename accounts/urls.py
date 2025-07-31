from django.urls import path, include
from . import views
urlpatterns = [
    path("join/", views.join, name="join"),
    path("dashboard/", include("dashboard.urls")),
    path("logout/", views.logout, name="logout"),
    path("confession/", include("confession.urls")),
    path("profile_page/", views.profile_page, name="profile_page"),
]