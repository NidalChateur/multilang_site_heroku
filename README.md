[![Python](https://raw.githubusercontent.com/NidalChateur/badges/779ce02cc0ce5bdc16ca2fe297b1229d4e5068d3/svg/python.svg)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/django-5.0.6-blue.svg?logo=django)](https://www.djangoproject.com/)
[![Poetry](https://img.shields.io/badge/poetry-1.8.3-blue.svg?logo=Poetry)](https://python-poetry.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/linting-flake8-yellowgreen.svg?logo=python)](https://github.com/pycqa/flake8)
[![Docker](https://img.shields.io/badge/dockerhub-images-important.svg?logo=docker)](https://hub.docker.com/r/nidalchateur/multilang_site)

#  <a href="https://multilang-site-1-joro.onrender.com">Blogs</a>

### Presentation 

Blogs is a multilingual deployed application built with :

- Django internationalization (i18n) for language support.
- Django Mail and JWT for password reset functionality.
- Django Admin to manage data.
- OpenAI chatbot for interactive user engagement.
- Cryptography to secure authenticated user data.
- JavaScript and Django REST Framework for dynamic search functionality.
- Pillow to resize and save blog images efficiently.
- Bootstrap for the frontend.

### Uses cases

- Logged-in users: You can change the current language (fr-en), create, read, update, and delete (CRUD) posts, and search through them. All of it is possible in the navigation.

- Visitors: You can change the current language (fr-en), read posts and search through the content. All of it is possible in the navigation.

### Run locally the app
0. Set environnement variables

1. Install decencies

    - `python -m venv env` or `python3 -m venv env`

    - `env/scripts/activate` or `source env/bin/activate`

    - `pip install -m requirements/dev_freeze.txt`

2. Apply migrations

    - `python manage.py migrate`

3. Run

    - `python manage.py runserver`

### Translation Steps Documentation (i18n)

0. Configure settings.py, templates and python files

    - settings.py :
    ```
        from django.utils.translation import gettext_lazy as _

        MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",

        # add this middleware used by i18n
        "django.middleware.locale.LocaleMiddleware",
        #

        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]


        LOCALE_PATHS = [
            BASE_DIR / "locale",
        ]


        LANGUAGES = [
            ("fr", _("French")),
            ("en", _("English")),
        ]


        LANGUAGE_CODE = "en"

        TIME_ZONE = "UTC"

        USE_I18N = True

        USE_TZ = True

        USE_L10N = True
    ```

    - templates (html files) :
    ```
    {% load i18n %}
    <p>{% translate 'No post' %}.</p>

    ``` 

    - forms.py and models.py :
    ```
        from django.utils.translation import gettext_lazy as _

        title=_("Title") 

    ```

    - views.py :
    ```
        from django.utils.translation import gettext as _

        title=_("Title") 

    ```

1. Create django.po files for manual translation

    `mkdir locale` 

    `py .\manage.py makemessages -l en --ignore=env/*` 

    `py .\manage.py makemessages -l fr --ignore=env/*`

2. Update django.po files (if modifications are made)

    `py .\manage.py makemessages -a --ignore=env/*`

3. Manually edit the django.po files for translation

    Open and edit the generated django.po files in the locale directory. Translate the message strings under each language's respective section (msgid for original text and msgstr for translations).

3. Compile translations

    `py .\manage.py compilemessages`
