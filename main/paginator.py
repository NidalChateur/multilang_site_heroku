from django.core.paginator import Paginator


def paginator(request, queryset, obj_per_page: int = 10) -> Paginator:
    """used to split querysets"""

    paginator = Paginator(queryset, obj_per_page)
    page_number = request.GET.get("page")

    return paginator.get_page(page_number)
