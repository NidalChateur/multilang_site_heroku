"""
URL configuration for multilang_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("api.urls")),
]

urlpatterns += i18n_patterns(
    path("", include("authentication.urls")),
    path("", include("main.urls")),
    path("", include("chatbot.urls")),
)

# image config
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# enabled if DEBUG=False
handler404 = "error.views.error_404"
handler403 = "error.views.error_403"
handler500 = "error.views.error_500"

# if the app is deployed
urlpatterns += staticfiles_urlpatterns()
