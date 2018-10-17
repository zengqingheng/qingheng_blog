# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 1:57
# @Author  : ZengQingheng
# @Email   : 1107753149@qq.com
# @File    : myfilter.py
# @Software: PyCharm
from django import template
register = template.Library()
#注册过滤器
@register.filter
def month_to_upper(key):
    return ['一','二','三','四','五','六','七','八','九','十','十一','十二',][key]