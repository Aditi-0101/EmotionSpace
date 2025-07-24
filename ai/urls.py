from django.urls import path, include
from . import views
urlpatterns = [
    path("ask_ai/", views.ask_ai, name="ask_ai"),
]