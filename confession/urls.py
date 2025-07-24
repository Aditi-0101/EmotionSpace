from django.urls import path, include
from . import views
urlpatterns = [
    path("create_confession/", views.create_confession, name="create_confession"),
    path("display_confession/", views.display_confession, name="display_confession"),
    path('delete_confession/<int:id>/', views.delete_confession, name='delete_confession'),
    path('update_confession/<int:id>/', views.update_confession, name='update_confession'),
]