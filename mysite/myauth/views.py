from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from .models import Profile


class ProfilesListView(ListView):
    template_name = 'myauth/users-list.html'
    queryset = Profile.objects.all()
    context_object_name = 'profiles'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "myauth/user-profile.html"
    model = Profile
    context_object_name = 'profile'


def profile_redirect(request: HttpRequest) -> HttpResponseRedirect:
    return redirect(reverse(
        "myauth:profile",
        kwargs={"pk": request.user.id}
    ))


class AvatarUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if (self.request.user.is_staff or
                self.request.user.id == self.get_object().user.id):
            return True
        return False

    model = Profile
    fields = 'avatar',
    template_name = 'myauth/avatar_update_form.html'

    def get_success_url(self):
        return reverse(
            "myauth:profile",
            kwargs={"pk": self.object.pk}
        )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)

        return response


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set!")
    response.set_cookie("fizz", "buzz", max_age=3600)

    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value {value!r}")


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")
