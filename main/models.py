import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image


class Post(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    slug_title = models.SlugField(null=True)

    publication_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def _rename_image(self):
        image = self.image
        unused_file_name, file_extension = os.path.splitext(image.name)
        # define relative path from BASE_DIR.MEDIA_ROOT
        self.image = f"post/{uuid.uuid4()}{file_extension}"

        return image

    def _image_has_changed(self) -> bool:
        """detect if the image posted in form is new"""

        if not self.image:
            # case 1 : no image in form
            return False

        if not self.id and self.image:
            # case 2 : create post
            return True

        if self.id:
            # case 3 : update
            post_in_db = Post.objects.filter(id=self.id).first()

            return post_in_db.image != self.image

    def resize_and_rename_image(self):
        if self._image_has_changed():
            image = self._rename_image()

            image = Image.open(image)

            # define here the new with
            IMAGE_MAX_WIDTH = 150
            IMAGE_MAX_HEIGHT = IMAGE_MAX_WIDTH

            # resize keeping the original ration
            image.thumbnail((IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))

            image.save(self.image.path)

    def save(self, request, *args, **kwargs):
        self.author = request.user
        self.slug_title = slugify(self.title)
        self.resize_and_rename_image()
        super().save(*args, **kwargs)
