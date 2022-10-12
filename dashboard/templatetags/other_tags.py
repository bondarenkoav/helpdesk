from datetime import datetime, timedelta
from django import template

__author__ = 'ipman'
register = template.Library()


@register.simple_tag()
def get_return_equipment_color_string_in_list(date_term, status):
    cur_date = datetime.now().date()
    if status == "open":
        if date_term <= cur_date:
            class_color = "danger"
        elif (cur_date >= (date_term - timedelta(days=3))) and (cur_date <= date_term):
            class_color = "warning"
        else:
            class_color = "success"
    elif status == "complete":
        class_color = "primary"
    else:
        class_color = "secondary"
    return class_color
