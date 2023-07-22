from django.views.generic import TemplateView


class AboutMeView(TemplateView):
    template_name = "myauth/user-profile.html"
