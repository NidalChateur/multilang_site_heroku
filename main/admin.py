from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "publication_date", "modification_date")


admin.site.register(Post, PostAdmin)
