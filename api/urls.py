from django.urls import path

from .views import SearchPostView

urlpatterns = [
    path("api/posts/", SearchPostView.as_view(), name="api_posts"),
]
