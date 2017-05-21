import celery
from mmwxapi.app.wechat.util import get_third_mp


@celery.shared_task(bind=True)
def send_wx_message(self, msg=None):
    mp = get_third_mp()

    # mp.send_news_message()
    mp.send_text_message("oVqdvxLWQtdcnY5sLa-HTnUJPyEg", "Test 1")
