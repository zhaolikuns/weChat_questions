from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r'^paper/([^/]+)/$', views.show_paper, name='show_paper'),
    url(r"^paper/([^/]+)/result/$", views.show_paper_result, name="show_paper_result"),
    url(r"^paper/([^/]+)/result/history/$", views.show_result_history, name="show_result_history"),
    url(r"^paper/([^/]+)/result/history/([^/]+)/$", views.show_result_detail, name='show_result_detail'),
    url(r"^result/history/$", views.show_result_history_all, name='show_result_history_all'),
]
