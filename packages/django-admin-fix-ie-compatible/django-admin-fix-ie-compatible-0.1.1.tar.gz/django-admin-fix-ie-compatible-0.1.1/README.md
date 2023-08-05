# django-admin-fix-ie-compatible

Add X-UA-Compatible meta to django's admin site, so that the admin site can work in IE's compatible mode under IE9 or high version.

## Install

```shell
pip install django-admin-fix-ie-compatible
```

## Settings

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_admin_fix_ie_compatible',
    ...
]
```

**Note:**

1. Just add django_admin_fix_ie_compatible to INSTALLED_APPS, and nothing more.

## Releases

### v0.1.1 2020/03/09

- Fix requirements.txt reading problem in setup.py.

### v0.1.0 2020/03/09

- First release.
