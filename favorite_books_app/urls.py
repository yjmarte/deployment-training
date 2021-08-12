"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^
from django.urls import path
from .import views


urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("books", views.show_all),
    path("books/create", views.create_book),
    path("books/<int:book_id>", views.show_one),
    path("books/<int:book_id>/update", views.update),
    path("books/<int:book_id>/delete", views.delete),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
    path("logout", views.logout)
]
, views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^
from django.urls import path
from .import views


urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("books", views.show_all),
    path("books/create", views.create_book),
    path("books/<int:book_id>", views.show_one),
    path("books/<int:book_id>/update", views.update),
    path("books/<int:book_id>/delete", views.delete),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
    path("logout", views.logout)
]
, Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from .import views


urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("books", views.books),
    path("books/favorited", views.favorited),
    path("books/create", views.create),
    path("books/<int:book_id>", views.retrieve),
    path("books/<int:book_id>/update", views.update),
    path("books/<int:book_id>/delete", views.delete),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
    path("logout", views.logout)
]