from django import forms
from django.core.validators import FileExtensionValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        widget=forms.TextInput({"placeholder": _("Title")}),
        validators=[MinLengthValidator(3)],
        required=True,
    )

    content = forms.CharField(
        label=_("Content"),
        widget=forms.Textarea({"placeholder": _("Content"), "rows": 5}),
        validators=[MinLengthValidator(3)],
        required=True,
    )

    image = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        required=False,
    )

    class Meta:
        model = Post
        fields = ("title", "content", "image")


class SearchPostForm(forms.Form):
    search = forms.CharField(label="", required=True)
