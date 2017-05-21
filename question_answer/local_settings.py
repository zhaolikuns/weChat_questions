from question_answer.settings import BASE_DIR

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{BASE_DIR}/question.db',
        'HOST': '127.0.0.1',
        # 'PORT': '5432',     默认端口 可以不用写
    }
}