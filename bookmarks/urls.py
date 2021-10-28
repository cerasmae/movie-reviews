from django.conf.urls import include, url
from . import views

urlpatterns = [
  url(r'^bookmarks-list/', views.bookmarks_view, name='bookmarks-list'),
  url(r'^create-folder/', views.create_folder, name='create-folder'),
  url(r'^create-bookmark/', views.create_bookmark, name='create-bookmark'),
  url(r'^delete-bookmark/', views.delete_bookmark, name='delete-bookmark'),
  url(r'^get-folders/', views.get_folders, name='get-folders'),
]