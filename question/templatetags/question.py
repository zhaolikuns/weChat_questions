from django.template import Library

register = Library()

@register.assignment_tag(name="is_user_selected")
def is_user_selected(result, question, answer):
    return result.is_user_selected(question, answer)

@register.simple_tag(name="user_result_desc")
def user_result_desc(result, question):
    return result.is_right_desc(question)
