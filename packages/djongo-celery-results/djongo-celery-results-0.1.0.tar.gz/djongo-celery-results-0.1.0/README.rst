djongo-celery-results/README.rst
=====
djongo-celery-results
=====

Djongo-celery-results is a complement to django-celery-djongo, based on
django-celery-results, preserving the structure of the model used in mysql,
but implemented for mongodb, and keeping the flow intact
for migrations from mysql to mongodb.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "Djongo-celery-results" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'djongo-celery-results',
    )

2. Run `python manage.py migrate` to create the djongo-celery-results models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to view the tasks (you will need the Admin application enabled).
