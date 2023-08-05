# Django JET

![image](https://raw.githubusercontent.com/geex-arts/jet/static/logo.png)


**what**|**where**
-----|-----
master tests|[![image][master-tests-badge]][master-tests]
dev tests|[![image][dev-tests-badge]][dev-tests]
live demo|http://demo.jet.geex-arts.com/admin/
documentation|http://jet.readthedocs.org/
PyPi|https://pypi.org/project/djet2

[master-tests]: https://github.com/vanyakosmos/djet2/actions?query=workflow%3Atest+branch%3Amaster
[master-tests-badge]: https://github.com/vanyakosmos/djet2/workflows/test/badge.svg?branch=master
[dev-tests]: https://github.com/vanyakosmos/djet2/actions?query=workflow%3Atest+branch%3Adev
[dev-tests-badge]: https://github.com/vanyakosmos/djet2/workflows/test/badge.svg?branch=dev


## Why Django JET?

- New fresh look
- Responsive mobile interface
- Useful admin home page
- Minimal template overriding
- Easy integration
- Themes support
- Autocompletion
- Handy controls

## Screenshots

![image](https://raw.githubusercontent.com/geex-arts/django-jet/static/screen1.png)

![image](https://raw.githubusercontent.com/geex-arts/django-jet/static/screen2.png)

![image](https://raw.githubusercontent.com/geex-arts/django-jet/static/screen3.png)

## Installation

- Download and install latest version of Django JET:

```bash
pip install djet2
```

- Add 'jet' application to the INSTALLED\_APPS setting of your Django project 
settings.py file (note it should be before 'django.contrib.admin'):

```python
INSTALLED_APPS = (
    ...,
    'jet',
    'django.contrib.admin',
)
```

- Make sure `django.template.context_processors.request` context processor 
is enabled in settings.py (Django 1.8+ way):

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ...,
                'django.template.context_processors.request',
                ...,
            ],
        },
    },
]
```

- Add URL-pattern to the urlpatterns of your Django project urls.py file 
(they are needed for related–lookups and autocompletes):

```python
urlpatterns = patterns(
    '',
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', include(admin.site.urls)),
    ...
)
```

- Create database tables:

```bash
python manage.py migrate jet
```

- Collect static if you are in production environment:

```bash
python manage.py collectstatic
```

- Clear your browser cache:
    - firefox/chrome: <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>) for hard reload

## Dashboard installation

Dashboard is located into a separate application. So after a typical JET 
installation it won't be active. To enable dashboard application follow these steps:

- Add 'jet.dashboard' application to the INSTALLED\_APPS setting of your Django 
project settings.py file (note it should be before 'jet'):

```python
INSTALLED_APPS = (
    ...,
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    ...,
)
```

- Add URL-pattern to the urlpatterns of your Django project urls.py file 
(they are needed for related–lookups and autocompletes):

```python
urlpatterns = patterns(
    '',
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', include(admin.site.urls)),
    ...,
)
```

- **For Google Analytics widgets only** install python package:

```bash
pip install djet2[google_analytics]
# or 
pip install google-api-python-client==1.4.1
```

- Create database tables:

```bash
python manage.py migrate dashboard
```

- Collect static if you are in production environment:

```bash
python manage.py collectstatic
```
