from django.apps import AppConfig
from django.conf import settings


class QuestionConfig(AppConfig):
    name = 'question'
    verbose_name = "题目管理"

    def ready(self):
        from mmwxapi.all import db

        db.setup_engine({
            "main": {
                "url": settings.MMWXAPI_SAURL,
            },
        })
