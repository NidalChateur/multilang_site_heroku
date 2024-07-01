from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import Post


class IsAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user = self.request.user
        current_path = self.request.path

        # get the post.id from the url
        post_id = (
            current_path.replace("/fr/posts/", "")
            .replace("/en/posts/", "")
            .replace("/update/", "")
            .replace("/delete/", "")
        )

        post = get_object_or_404(Post, id=int(post_id))

        return user.id == post.author.id
