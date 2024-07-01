from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from .forms import PostForm, SearchPostForm
from .models import Post
from .paginator import paginator
from .permissions import IsAuthorRequiredMixin


class SearchPost(View):
    def post(self, request):
        form = SearchPostForm(request.POST)

        if form.is_valid():
            search = form.cleaned_data.get("search")
            posts_url = reverse("posts")
            # search_url = /posts/?search=...
            search_url = f"{posts_url}?search={search}"

            return redirect(search_url)


class UserPosts(View):
    """redirect to user posts list"""

    def get(self, request, user_id):
        posts_url = reverse("posts")
        # user_posts_url = /posts/?user_id=...
        user_posts_url = f"{posts_url}?user_id={user_id}"

        return redirect(user_posts_url)


class ListPosts(View):
    def get(self, request):
        # get parameters from url
        search = request.GET.get("search")
        user_id = request.GET.get("user_id")

        if search:
            posts = Post.objects.filter(slug_title__icontains=search).order_by(
                "-modification_date"
            )
        elif user_id and user_id.isdigit():
            posts = Post.objects.filter(author__id=int(user_id)).order_by(
                "-modification_date"
            )
        else:
            posts = Post.objects.all().order_by("-modification_date")

        page_obj = paginator(request, posts, obj_per_page=10)

        return render(request, "posts_list.html", {"page_obj": page_obj})


class DetailPost(View):
    def get(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)

        return render(request, "post_detail.html", {"post": post})


class CreatePost(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()

        return render(request, "post_create.html", {"form": form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save(request)

            messages.success(request, _("Post created successfully."))

            return redirect("posts")

        return render(request, "post_create.html", {"form": form})


class UpdatePost(LoginRequiredMixin, IsAuthorRequiredMixin, View):
    def get(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=post)

        return render(request, "post_update.html", {"form": form})

    def post(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save(request)

            messages.success(request, _("Post updated successfully."))

            return redirect("post", post.id)

        return render(request, "post_update.html", {"form": form})


class DeletePost(LoginRequiredMixin, IsAuthorRequiredMixin, View):
    def post(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, _("Post deleted successfully."))

        return redirect("posts")
