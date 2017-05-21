from hmiku import *
from django.shortcuts import get_object_or_404, redirect, Http404
from django.db import transaction
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from mmwxapi.app.wechat.decorators import wechat_login_required
from django.contrib.auth.decorators import login_required

from .models import Paper, Result
from .forms import ResultDetailFormSet

_log = mm.log.getLogger(__name__)


@wechat_login_required
@login_required
@transaction.atomic
def show_paper(request, pid):
    paper = get_object_or_404(Paper, pk=pid, is_publish=True)

    result = paper.result.filter(user=request.user).first()
    if result is not None:
        return redirect(reverse("show_result_detail", args=(pid, result.id)))

    if request.method == "POST":
        formset = ResultDetailFormSet(request.POST,
                                      initial=[{"question": paper_detail.question,
                                                "answer": []}
                                               for paper_detail in paper.detail.all()],
                                      paper=paper)

        if formset.is_valid():
            result = Result.objects.create(user=request.user, paper=paper)
            for form in formset.forms:
                question = form.cleaned_data["question"]
                answer_list = form.cleaned_data["answer"]
                result.add_result(question, answer_list)

            result.compile_total_score()
            result.save()

            return redirect(reverse("show_paper_result", args=(pid,)))

        _log.error(f"formset.errors: {formset.errors}")

    else:
        formset = ResultDetailFormSet(initial=[{"question": paper_detail.question,
                                                "answer": []}
                                               for paper_detail in paper.detail.all()],
                                      paper=paper)

    return TemplateResponse(request, "question/paper.html",
                            {
                                "paper": paper,
                                "formset": formset,
                            })


@wechat_login_required
@login_required
def show_paper_result(request, pid):
    paper = get_object_or_404(Paper, pk=pid, is_publish=True)
    result = paper.get_last_result_by_user(user=request.user)
    if result is None:
        #用户还没有答过这个试卷, 则跳转到答题页
        return redirect(reverse("show_paper", args=(pid,)))

    return TemplateResponse(request, "question/result.html",
                            {
                                "paper": paper,
                                "result": result,
                            })


@wechat_login_required
@login_required
def show_result_history(request, pid):
    """\
    显示一个试卷的答题结果历史
    """
    paper = get_object_or_404(Paper, pk=pid, is_publish=True)
    resultl = paper.result.filter(user=request.user).all()

    return TemplateResponse(request, "question/result_history.html",
                            {
                                "paper": paper,
                                "resultl": resultl,
                            })


@wechat_login_required
@login_required
def show_result_detail(request, pid, rid):
    """\
    显示某次答题结果的详细信息,
    """
    paper = get_object_or_404(Paper, pk=pid, is_publish=True)
    result = get_object_or_404(paper.result.all(), user=request.user, pk=rid)

    return TemplateResponse(request, "question/result_detail.html",
                            {
                                "paper": paper,
                                "result": result,
                            })


@wechat_login_required
@login_required
def index(request):
    last_paper = Paper.objects.order_by("-id").first()
    if last_paper is None:
        return Http404

    return redirect(reverse("show_paper", args=(last_paper.id,)))


@wechat_login_required
@login_required
def show_result_history_all(request):
    """\
    显示所有试卷的最后一次作答历史的一个列表
    """
    history_list = []
    for paper in Paper.objects.order_by("-id").all():
        history_list.append({
            "paper": paper,
            "last_result": paper.result.filter(user=request.user).first(),
        })

    return TemplateResponse(request, "question/show_result_history_all.html",
                            {
                                "history_list": history_list,
                            })
