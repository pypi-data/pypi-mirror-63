This app patches the following cms issues:
- https://github.com/divio/django-cms/issues/6622
- https://github.com/divio/django-cms/issues/6433

And contains sentry 500 error handler with an advanced send_email function.

Installation
============

Run `pip install djangocms-helpers`.

Update `INSTALLED_APPS` with :

    INSTALLED_APPS = [
        ...
        'djangocms_helpers',
        ...
    ]

