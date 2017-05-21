from django.contrib import admin

from .models import Question, Answer, Paper, Result, PaperDetail, ResultDetail
from .forms import AnswerAdminInlineFormSet


class AnswerInline(admin.TabularInline):
    model = Answer
    min_num = 2
    extra = 0
    can_delete = True
    formset = AnswerAdminInlineFormSet

    fields = ["is_right", "content", ]


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['name', "is_multiple_admin_field", ]

    readonly_fields = ["is_multiple_admin_field", ]

    inlines = [AnswerInline, ]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields[1:]

        return self.readonly_fields


class PaperQuestionInline(admin.TabularInline):
    model = PaperDetail
    min_num = 0
    extra = 0
    can_delete = False

    fields = ["question", ]

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.result.exists():
            self.can_delete = False
            self.can_add = False
            return self.readonly_fields + ("question",)

        return self.readonly_fields


class PaperAdmin(admin.ModelAdmin):
    list_display = ["title", "is_publish", "question_count", ]

    inlines = [PaperQuestionInline, ]

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.result.exists():
            return self.readonly_fields + ("title", "is_publish",)

        return self.readonly_fields


class ResultDetailInline(admin.TabularInline):
    model = ResultDetail
    extra = 0
    can_delete = False

    readonly_fields = fields = ["question_index", "answer_index", ]

    def has_add_permission(self, *args, **kwargs):
        return False
        #
        # def has_change_permission(self, *args, **kwargs):
        #     return False


class ResultAdmin(admin.ModelAdmin):
    list_display = ("user", "paper",)

    readonly_fields = ["score", ]

    fieldsets = [
        (None, {
            "fields": ["score", ],
        })
    ]

    inlines = [ResultDetailInline, ]

    def has_add_permission(self, obj=None, *args, **kwargs):
        return obj == None


admin.site.register(Question, QuestionAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Result, ResultAdmin)
