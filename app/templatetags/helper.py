from django import template
from datetime import datetime
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.filter
def display_sex(value):
    SEXES = { 1 : "男性", 2 : "女性" }
    return SEXES[value]

@register.inclusion_tag("app/shered/pulldown_link.html")
def pulldonw_link(contents):
    today = datetime.today()
    links = []

    for i in range(4):
      date = today + relativedelta(months=-i)
      links.append([date.strftime('%Y/%-m'), date.strftime('%Y年 %-m月')])

    return { 'contents': contents, 'links': links }

@register.inclusion_tag("app/shered/navbar.html")
def navbar(*args):
    return { 'args': args }
