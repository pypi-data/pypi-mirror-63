=========
Taskboard
=========
Quick start
-----------
1. Include the URLconf in your project urls.py::

    path('taskboard/', include('taskboard.urls')),


2. Include the app in your project settings.py::

    INSTALLED_APPS = [
        'taskboard.apps.Taskboard',
    ]


3. Configure the session engine in your project settings.py::

    SESSION_ENGINE = 'django.contrib.sessions.backends.file',


4. Configure the admins object in your project settings.py::

    TASKBOARD_ADMINS = [
        {'username': 'admin', 'password': 'admin', 'name': 'Administrator'},
    ]


5. Visit http://127.0.0.1:8000/taskboard/ to open the dashboard.

Build
-----
1. python setup.py sdist
2. twine upload dist/*
