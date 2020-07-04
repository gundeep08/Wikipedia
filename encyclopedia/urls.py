from django.urls import path
from . import views

urlpatterns = [
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("<str:name>", views.entry, name="entry"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("", views.index, name="index")
]
