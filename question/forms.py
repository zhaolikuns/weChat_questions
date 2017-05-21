from django import forms


class AnswerAdminInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(AnswerAdminInlineFormSet, self).clean()

        for form_data in self.cleaned_data:
            if form_data["is_right"]:
                break
        else:
            self._non_form_errors.append(forms.ValidationError("必须至少有一个正确答案", "no_right_answer"))


class ResultDetailForm(forms.Form):
    question = forms.ModelChoiceField(None)
    answer = forms.ModelMultipleChoiceField(None)

    def __init__(self, paper, qid, *args, **kwargs):
        super(ResultDetailForm, self).__init__(*args, **kwargs)

        question = paper.question.get(pk=qid)

        self.fields["question"].queryset = paper.question.all()
        self.fields["question"].initial = question

        self.fields["answer"].queryset = question.answer.all()


class ResultDetailFormSet(forms.formset_factory(form=ResultDetailForm, extra=0,
                                                can_delete=False, can_order=False, )):
    @property
    def paper_detail(self):
        return self.paper.detail.all()

    def __init__(self, *args, paper=None, **kwargs):
        self.paper = paper
        super(ResultDetailFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        default = {
            "qid": self.paper_detail[i].question.id,
            "paper": self.paper,
        }

        default.update(kwargs)

        return super(ResultDetailFormSet, self)._construct_form(i, **default)
