from hmiku import *
mm.log.set_verbose(3)

#激活 celery app, 否则 shared_task 将无法 bind 到这个 app
from .celery import app as celery_app
