from django.urls import path

from .views import ArticlesListView


app_name = "shopapp"

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles_list"),
]
