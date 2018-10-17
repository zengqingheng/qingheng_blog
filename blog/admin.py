from django.contrib import admin
from .models import *
#from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','desc','click_count',)#哪些字段显示在后台信息
    list_editable = ('click_count',)#可修改
    list_display_links = ('desc',)#点击可跳转修改
    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
#admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)

admin.site.register(Article,ArticleAdmin)