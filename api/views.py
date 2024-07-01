from rest_framework.generics import ListAPIView

from main.models import Post

from .serializers import PostSerializer


class SearchPostView(ListAPIView):
    """
    Read only (list view)

    Return the first ten results of the post search : slug_title search field.
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        # endpoint : localhost:8000/api/posts/?search=...
        search = self.request.GET.get("search")
        if search:
            return Post.objects.filter(slug_title__icontains=search).order_by(
                "-modification_date"
            )[:10]
