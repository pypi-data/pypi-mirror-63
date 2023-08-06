=========
Taskboard
=========

Quick start
-----------
1. Add "taskboard" to your INSTALLED_APPS setting like this::
    INSTALLED_APPS = [
        'taskboard'

    ]

2. Include the URLconf in your project urls.py::
    path('taskboard/', include('taskboard.urls'))

3. Configure the SESSION_ENGINE in your project settings.py::
    SESSION_ENGINE = 'django.contrib.sessions.backends.file'

4. Configure the TASKBOARD_ADMINS in your project settings.py::
    TASKBOARD_ADMINS = [
        {'username': 'admin', 'password': 'admin', 'name': 'Administrator'}

    ]

5. Visit http://127.0.0.1:8000/taskboard/ to open the dashboard.

Build
-----
1. python setup.py sdist
2. twine upload dist/*
