import decimal
import json
from functools import lru_cache

from django.db import models
from django.conf import settings

_log = mm.log.getLogger(__name__)


class Question(models.Model):
    ANSWER_IS_RIGHT = 0
    ANSWER_IS_WRONG = 1
    ANSWER_IS_HALFRIGHT = 2

    name = models.TextField(verbose_name="题目", max_length=1024)

    class Meta:
        verbose_name = verbose_name_plural = "题目"
        ordering = ["id", ]

    @property
    def is_multiple(self):
        return len(self.right_answer) > 1

    def is_multiple_admin_field(self):
        return self.is_multiple

    is_multiple_admin_field.short_description = "多选题"
    is_multiple_admin_field.boolean = True

    @property
    def right_answer(self):
        return [ans for ans in self.answer.all() if ans.is_right]

    @property
    def right_answer_id(self):
        return [ans.id for ans in self.right_answer]

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__str__()}>"

    def is_right(self, answer_list):
        """\
        判断答案是否正确,

        :returns:
            0:正确, 1:错误, 2:半对半错
        """
        if self.is_multiple:
            if set(self.right_answer_id) - set(answer_list):
                return self.ANSWER_IS_HALFRIGHT
            else:
                return self.ANSWER_IS_RIGHT
        else:
            #不是多选题, 却提供了多个答案
            if len(answer_list) > 1:
                return self.ANSWER_IS_WRONG

            if self.right_answer_id == answer_list:
                return self.ANSWER_IS_RIGHT
            else:
                return self.ANSWER_IS_WRONG


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answer")
    content = models.TextField(verbose_name="答案内容", max_length=1024)
    is_right = models.BooleanField(verbose_name="正确答案", default=False)

    class Meta:
        verbose_name = verbose_name_plural = "答案"

    def __str__(self):
        return f""

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__str__()}>"


class Paper(models.Model):
    title = models.CharField(verbose_name="标题", max_length=128, default="",
                             help_text="试卷标题, 比如 `第一学期期末测试题` 之类, 可以为空")

    question = models.ManyToManyField(Question, related_name="paper", through="PaperDetail")
    is_publish = models.BooleanField(verbose_name="已发布", default=False,
                                     help_text="未发布的试卷无法从前台访问作答")

    class Meta:
        verbose_name = verbose_name_plural = "试卷"

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__str__()}>"

    def question_count(self):
        return self.detail.count()

    question_count.short_description = "题目数"

    @lru_cache()
    def get_question_by_id(self, pid):
        """\
        根据 question id 返回 Question 对象
        """
        for d in self.detail.all():
            if d.question.id == pid:
                return d.question

    def get_last_result_by_user(self, user):
        """\
        获取用户的最后一次答题结果, 没有就是 None
        """
        return self.result.filter(user=user).order_by("-btime").first()


class PaperDetail(models.Model):
    paper = models.ForeignKey(Paper, related_name="detail")
    question = models.ForeignKey(Question, verbose_name="问题")

    class Meta:
        verbose_name = verbose_name_plural = "试卷题目"
        ordering = ["id", ]

    def __str__(self):
        return ""

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


class Result(models.Model):
    """\
    试卷的答题结果
    """
    TOTAL_SCORE = decimal.Decimal(100)

    #计算分数的因子,
    #每道题的得分为 题本身的分数 在 正确时, *1, 错误时, *0, 半对半错时, *0.5
    FACTOR_RIGHT = 1
    FACTOR_WRONG = 0
    FACTOR_HALFRIGHT = decimal.Decimal("0.5")

    ANSWER_DESC_RIGHT = "正确"
    ANSWER_DESC_WRONG = "错误"
    ANSWER_DESC_HALFRIGHT = "半对半错"

    paper = models.ForeignKey(Paper, related_name="result")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="score")
    btime = models.DateTimeField(verbose_name='答题日期', auto_now_add=True)

    score = models.DecimalField(verbose_name="总分", decimal_places=2, max_digits=20,
                                null=True, default=None, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "答题结果"
        ordering = ["-btime", "paper", "user"]

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__str__()}>"

    def add_result(self, question, answerl):
        """\
        添加一道题的答案,
        """
        result_detail = ResultDetail(question_index=question.id, answer_index=[a.id for a in answerl])
        self.detail.add(result_detail)

    def compile_total_score(self):
        """\
        根据当前答案计算总分
        """
        if self.detail.count() != self.paper.question_count():
            raise ValueError("count(result.answer) != count(paper.question)")

        score_total = 0
        score_per_ques = self.TOTAL_SCORE / self.detail.count()
        for d in self.detail.all():
            result = d.is_right()
            if result == Question.ANSWER_IS_RIGHT:
                score_total += score_per_ques * self.FACTOR_RIGHT
            elif result == Question.ANSWER_IS_WRONG:
                score_total += score_per_ques * self.FACTOR_WRONG
            elif result == Question.ANSWER_IS_HALFRIGHT:
                score_total += score_per_ques * self.FACTOR_HALFRIGHT

        self.score = score_total
        return score_total

    @lru_cache()
    def _answer_counter(self, t):
        """\
        根据结果类型, 计算统计信息,
        
        正确数量, 错误数量, 半对半错数量
        """
        return len([1 for d in self.detail.all() if d.is_right() == t])

    @property
    def count_right(self):
        """\
        正确的数量
        """
        print("zzz!")
        return self._answer_counter(Question.ANSWER_IS_RIGHT)

    @property
    def count_halfright(self):
        """\
        半对半错的数量
        """
        return self._answer_counter(Question.ANSWER_IS_HALFRIGHT)

    @property
    def count_wrong(self):
        return self._answer_counter(Question.ANSWER_IS_WRONG)

    @property
    def correct_rate(self):
        """\
        正确率, 半对半错算 0.5,
        
        返回 百分比
        """
        return ((self.count_right + decimal.Decimal("0.5") * self.count_halfright) / self.detail.count()) * 100

    def is_user_selected(self, question, answer):
        """\
        用户的指定题目是否选择了这个答案
        """
        result = self.detail.filter(question_index=question.id).first()
        answer_index = json.loads(result.answer_index)
        return answer.id in answer_index

    def is_right_desc(self, question):
        """\
        用户指定题目的作答情况, 返回 正确/错误/半对半错
        """
        detail = self.detail.filter(question_index=question.id).first()
        r = detail.is_right()
        if r == Question.ANSWER_IS_RIGHT:
            return self.ANSWER_DESC_RIGHT
        elif r == Question.ANSWER_IS_WRONG:
            return self.ANSWER_DESC_WRONG
        elif r == Question.ANSWER_IS_HALFRIGHT:
            return self.ANSWER_DESC_HALFRIGHT


class ResultDetail(models.Model):
    score = models.ForeignKey(Result, related_name="detail")

    question_index = models.IntegerField(verbose_name="题目", help_text="题目的ID")

    #用户提交的答案, 正确与否是未知的, 并且为了实现多选的题, 所以这里使用 int 列表字段（逗号分隔的整数字段）
    answer_index = models.CommaSeparatedIntegerField(verbose_name="用户提交的答案",
                                                     max_length=128)

    def is_right(self):
        """\
        判断这个答案是否正确,

        :returns:
            由于有多选题的存在, 所以答案并不简单的是 对与错, 而还有半对半错,
            所以, 0:正确, 1:错误, 2:半对半错, 3:问题被删除
        """
        question = self.score.paper.get_question_by_id(self.question_index)
        if question is None:
            _log.warning("question was deleted")
            return 3

        answer_index = json.loads(self.answer_index)
        return question.is_right(answer_index)
