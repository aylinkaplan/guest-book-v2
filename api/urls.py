from django.urls import path

from api import views

urlpatterns = [
    path('entries/', views.EntryListView.as_view(), name='list-entry'),
    path('create_entry/', views.CreateEntryView.as_view(), name='create-entry'),
    path('users/', views.UserListView.as_view(), name='list-user'),
]