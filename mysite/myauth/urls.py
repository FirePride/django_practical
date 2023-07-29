from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    set_cookie_view, get_cookie_view,
    set_session_view, get_session_view,
    MyLogoutView,
    ProfileDetailView,
    AvatarUpdateView,
    RegisterView,
    ProfilesListView,
    AboutMeView,
)


app_name = "myauth"

urlpatterns = [
    path("", ProfilesListView.as_view(), name='profiles'),
    path("login/",
         LoginView.as_view(
             template_name='myauth/login.html',
             redirect_authenticated_user=True
         ),
         name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("profile/", AboutMeView.as_view(), name="about-me"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("profile/<int:pk>/avatar/", AvatarUpdateView.as_view(), name="avatar"),
    path("register/", RegisterView.as_view(), name="register"),

    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),

    path("session/set/", set_session_view, name="session_set"),
    path("session/get/", get_session_view, name="session_get"),
]
