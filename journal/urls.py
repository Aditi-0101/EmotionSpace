from django.urls import path, include
from . import views
urlpatterns = [
    path('create_journal/',views.create_journal,name="create_journal"),
    path('read_journal/',views.read_journal,name="read_journals"),
    path('read_journal/<int:entry_id>/',views.read_journal,name="read_journal"),
    path('delete_journal/<int:id>/', views.delete_journal, name='delete_journal'),
    path('edit_journal/<int:id>/', views.edit_journal, name='edit_journal'),
]