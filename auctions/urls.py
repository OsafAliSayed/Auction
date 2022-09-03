from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item/<str:name>", views.itempage, name="itempage"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.display_category, name="display_category")
]
