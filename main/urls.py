from django.urls import path

from .views import (
    CreatePost,
    DeletePost,
    DetailPost,
    ListPosts,
    SearchPost,
    UpdatePost,
    UserPosts,
)

urlpatterns = [
    path("", ListPosts.as_view(), name="home"),
    path("posts/", ListPosts.as_view(), name="posts"),
    path("posts/search/", SearchPost.as_view(), name="search_post"),
    path("posts/user/<int:user_id>/", UserPosts.as_view(), name="user_posts"),
    path("posts/<int:post_id>/", DetailPost.as_view(), name="post"),
    path("posts/create/", CreatePost.as_view(), name="create_post"),
    path("posts/<int:post_id>/update/", UpdatePost.as_view(), name="update_post"),
    path("posts/<int:post_id>/delete/", DeletePost.as_view(), name="delete_post"),
]
