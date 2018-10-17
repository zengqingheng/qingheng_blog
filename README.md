# qingheng_blog
这个项目是Django个人博客项目，静态文件是从网上找的。
1、使用的数据库为mysql，项目目前还没有部署到服务器。
在setting.py里面设置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qinghengblogdb',
        'USER':'username',
        "PASSWORD":"******",
    }
}
2、所有者可在后台创建发布文章，文章的model设计如下
在app的models.py中
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户',on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类',on_delete=models.CASCADE,)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    objects = ArticleManager() #自定义manager管理器

    # 更新浏览量
    def viewed(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title
    其它model，如广告，标签，分类，友情链接，用户，都是在这个文件里面定义的。
 3、然后是关于views.py
 
 #这个函数是将一个在不同模板中都会用的一些从数据库中返回的数据，统一返回便于管理
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

#这个是首页的函数
def index(request):
    try:
        #最新文章数据
        Article_list = get_page(request,Article.objects.all())
    except Exception as e:
        # print(e)
        logger.error(e)
    return render(request,'index.html',locals())
    
#这个是按时间归档的函数
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
#这个是按标签归档的函数
def tag_archive(request):
    tag = request.GET.get('tag')
    Article_list = Article.objects.filter(tag__name__contains=tag)
    Article_list = get_page(request,Article_list)
    return render(request,'tag_archive.html',locals())

#这个是查看文章时的函数
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

#为了防止代码冗余，添加了这段代码，把分页器的代码放到这里
def get_page(request,article_list):
    paginator = Paginator(article_list,2)
    try:
        page = request.GET.get('page', 1)
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list
    
  4、对于模板，把各个页面通用的部分放到base.html,其它模板再从这个模板继承，
  另外一些常用的功能，也被做成了小模板，在需要用到的时候，使用{%include "xxx.html"%}进行引入。
  如广告，分页。
  5、当找不到需要的页面时，会进入设定的failure.html
