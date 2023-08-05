=========
Taskboard
=========

Quick start
-----------

1. Add "taskboard" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'taskboard',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('taskboard/', include('taskboard.urls')),

3. Visit http://127.0.0.1:8000/taskboard/ to open the dashboard.

Build
-----

1. python setup.py sdist
2. twine upload dist/*
