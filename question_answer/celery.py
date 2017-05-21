import os
from celery import Celery

app = Celery()

if "DJANGO_SETTINGS_MODULE" in os.environ:
    app.config_from_object("question_answer.settings")

else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "question_answer.settings")

    import django
    django.setup()

    app.config_from_object("question_answer.settings")

app.conf.timezone = "Asia/Shanghai"

app.autodiscover_tasks(["question.tasks"])
