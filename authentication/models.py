import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from multilang_site.utils.encryptor import Encryptor


class User(AbstractUser):
    # to set email as USERNAME_FIELD :
    # USERNAME_FIELD = "email" ( /!\ email is currently encrypted )
    # REQUIRED_FIELDS = ["username"]

    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    image = models.ImageField(null=True, blank=True, max_length=255)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username

    def _rename_image(self):
        image = self.image
        unused_file_name, file_extension = os.path.splitext(image.name)
        # define relative path from BASE_DIR.MEDIA_ROOT
        self.image = f"user/{uuid.uuid4()}{file_extension}"

        return image

    def _image_has_changed(self) -> bool:
        """detect if the image posted in form is new"""

        if not self.image:
            # case 1 : no image in form
            return False

        if not self.id and self.image:
            # case 2 : signup
            return True

        if self.id:
            # case 3 : update
            user_in_db = User.objects.filter(id=self.id).first()
            user_in_db.decrypt()

            return user_in_db.image != self.image

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

    def encrypt(self):
        """encrypt user data"""

        self.email = Encryptor.encrypt(self.email)
        self.first_name = Encryptor.encrypt(self.first_name)
        self.last_name = Encryptor.encrypt(self.last_name)
        if self.image:
            self.image.name = Encryptor.encrypt(self.image.name)

    def decrypt(self):
        """decrypt user data"""

        self.email = Encryptor.decrypt(self.email)
        self.first_name = Encryptor.decrypt(self.first_name)
        self.last_name = Encryptor.decrypt(self.last_name)
        if self.image:
            self.image.name = Encryptor.decrypt(self.image.name)

    def save(self, *args, **kwargs):
        self.resize_and_rename_image()
        self.encrypt()
        super().save(*args, **kwargs)
