from django.shortcuts import render
import logging
from .models import Category,Ad,Article,Comment,Tag,Links
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.conf import settings
from django.db.models import Count
logger = logging.getLogger('blog.views')
# Create your views here.

def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    GIT_HUB   = settings.GITHUB
    EMAIL = settings.EMAIL
    # 分类信息获取
    Category_list = Category.objects.all()
    # 广告数据
    Ad_list = Ad.objects.all()
    #归档数据获取
    archive_list = Article.objects.distinct_date()
    #标签云
    article_tag_list = Tag.objects.all()
    #友情链接
    link_list = Links.objects.all()
    #站长推荐
    article_recommend_list = Article.objects.filter(is_recommend=1).order_by('is_recommend')[0:6]
    #文章排行榜
    article_click_count_list = Article.objects.all().order_by('-click_count')[0:6]
    #评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count = Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()

def index(request):
    try:
        #最新文章数据
        Article_list = get_page(request,Article.objects.all())
    except Exception as e:
        # print(e)
        logger.error(e)
    return render(request,'index.html',locals())

def archive(request):
    try:
        #先获取客户端链接的信息
        year = request.GET.get('year',None)
        month= request.GET.get('month',None)
        Article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)#
        Article_list = get_page(request,Article_list)
        archive_list = Article.objects.distinct_date()
    except Exception as e:
        logger.error(e)
    # print('locals:',locals())
    return render(request,'archive.html',locals())

def tag_archive(request):
    tag = request.GET.get('tag')
    Article_list = Article.objects.filter(tag__name__contains=tag)
    Article_list = get_page(request,Article_list)
    return render(request,'tag_archive.html',locals())

def article(request):
    try:
        #获取文章id
        id = request.GET.get('id',None)
        try:
            article = Article.objects.get(pk=id)
            article.viewed()#浏览量+1
        except Article.DoesNotExist:
            return render(request,'failure.html',{'reason':'没有找到相应的文章'})
    except Exception as e:
        print(e)
    return render(request,'article.html',locals())



def get_page(request,article_list):
    paginator = Paginator(article_list,2)
    try:
        page = request.GET.get('page', 1)
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list
