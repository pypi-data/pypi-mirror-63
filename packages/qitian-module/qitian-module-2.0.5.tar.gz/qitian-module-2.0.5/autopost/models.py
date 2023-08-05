from django.db import models
from django.utils.html import format_html
from django.contrib.sites.models import Site
from smart_selects.db_fields import ChainedForeignKey
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from simditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from uuslug import uuslug


class AutoTask(models.Model):
    title = models.CharField('任务名称', max_length=128)
    crontab = models.CharField('定时任务', max_length=64, help_text='分 时 天 月 周', blank=True, null=True)
    url = models.CharField('抓取页面', max_length=255, blank=True, null=True)
    list_selector = models.CharField('列表规则', max_length=255, blank=True)
    page_selector = models.CharField('分页规则', max_length=255, blank=True)
    title_selector = models.CharField('标题规则', max_length=128, blank=True)
    title_replace = models.TextField('标题替换', help_text='以JSON数组,类似[("eee","ffff"),(444, "opt")]', blank=True)
    thumbnail_selector = models.CharField('缩略图规则', max_length=128, blank=True)
    content_selector = models.CharField('内容规则', max_length=128, blank=True)
    content_replace = models.TextField('内容替换', help_text='以JSON数组,类似[("eee","ffff"),(444, "opt")]', blank=True)
    content_except = models.CharField('内容排除', help_text='以json格式', max_length=255, blank=True, null=True, default='[]')
    lazy_photo = models.CharField('图片SRC属性', help_text='有延时图片时,不取src值,使用图片其它属性', max_length=128, blank=True, null=True,
                                  default='')
    source = models.CharField('来源设定', max_length=128, blank=True)
    author = models.ForeignKey('Author', verbose_name='作者', on_delete=models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, blank=True, null=True)
    category = ChainedForeignKey('Category', verbose_name='所属分类', chained_field='site', chained_model_field='site',
                                 auto_choose=True)
    enable = models.BooleanField('是否可用', choices=((True, '激活'), (False, '禁用')), default=True)
    crontab_key = models.CharField('定时任务KEY', max_length=62, blank=True, null=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def preview_title_btn(self):
        return format_html('<a href="####" onclick="title_preview()" id="title_preview_a">预览列表</a>')

    preview_title_btn.allow_tags = True
    preview_title_btn.short_description = '预览'

    def preview_detail_btn(self):
        return format_html('<a href="####" onclick="detail_preview()" id="detail_preview_a">预览内容</a>')

    preview_detail_btn.allow_tags = True
    preview_detail_btn.short_description = '预览内容'

    def operate_crawl(self):
        op_html = '<a href="###" onclick="crawl_news({id})">执行</a><br/>' \
                  '<a href="###" onclick="copy_task({id})">复制</a>'
        return format_html(op_html.format(id=self.id))

    operate_crawl.short_description = '操作'

    class Meta:
        db_table = 'at_auto_task'
        verbose_name = '自动抓取'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.title


class CrawlLogs(models.Model):
    title = models.CharField('文章标题', max_length=255)
    url = models.CharField('文章URL', max_length=255)
    site_url = models.CharField('站点URL', max_length=128, blank=True, null=True)
    status = models.IntegerField('状态', choices=((1, '新增'), (2, '已抓取'), (3, '已修改')), default=1)
    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'at_crawl_logs'
        verbose_name = '抓取记录'
        verbose_name_plural = verbose_name + "管理"
        ordering = ['-id']

    def __str__(self):
        return self.title


class Category(MPTTModel):
    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, default=1)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, verbose_name='上级菜单',
                            on_delete=models.DO_NOTHING)
    name = models.CharField('名称', max_length=64)
    desc = models.TextField('描述', blank=True, null=True)
    status = models.IntegerField('状态', choices={(0, '隐藏'), (1, '显示'), (2, '主菜单')}, default=1)
    # 需要一个站点唯一
    slug = models.CharField('标识', max_length=128, blank=True)
    url = models.CharField('地址', max_length=255, blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['id']
        get_ancestors = True

    class Meta:
        db_table = 'at_category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name + '管理'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuslug(self.name, self, max_length=128)
        return super().save(*args, **kwargs)

    def get_slug_list(self):
        """
        获取分类树，按照主在前的顺序
        :return:
        """
        return [(i.slug, i.name) for i in self.get_ancestors(include_self=True)]

    @staticmethod
    def get_tree_by_site(site, separator='-'):
        if not isinstance(site, Site):
            site = Site.objects.get(pk=site)
        root_node = Category.objects.filter(site=site, parent__isnull=True).all()
        all_tree = list()
        for category in root_node:
            child_node = category.get_family()
            node_info = [{'slug': node.slug, 'id': node.id, 'name': separator * node.get_level() + node.name} for node
                         in child_node]
            all_tree.append(node_info)
        return all_tree

    def __str__(self):
        return self.name + '[%s]' % self.site.name


class Author(models.Model):
    name = models.CharField('名称', max_length=64)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'at_author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name + '管理'

    def __str__(self):
        return self.name


class Article(models.Model):
    RC_TYPE = (
        (0, '不推荐'),
        (1, '幻灯'),
        (2, '焦点'),
        (3, '一级'),
        (4, '二级'),
        (5, '三级'),
    )

    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, default=1)
    category = TreeForeignKey(Category, related_name='category', null=True, blank=True, verbose_name='所属分类',
                              on_delete=models.DO_NOTHING)
    title = models.CharField('标题', max_length=255, db_index=True)
    summery = models.TextField('摘要', blank=True, null=True)
    content = RichTextField('内容', blank=True, null=True)
    keywords = models.CharField('关键词', max_length=255, blank=True, null=True)
    author = models.ForeignKey('Author', verbose_name='作者', on_delete=models.DO_NOTHING, default=1)
    type = models.IntegerField('文章类别', choices=((1, '文章'), (2, '外链'), (3, '内链')), default=1)
    link_address = models.CharField('外链地址', max_length=128, blank=True, null=True)
    recommend_type = models.IntegerField('推荐类别', choices=RC_TYPE, default=0)
    thumbnail = models.ImageField('缩略图', upload_to='thumbnail/%Y/%m/%d', blank=True)
    visits = models.IntegerField('访问数', default=1, blank=True)
    clear_link = models.BooleanField('清理链接', choices=((True, '是'), (False, '否')), default=True)
    save_img = models.BooleanField('保存图片', choices=((True, '是'), (False, '否')), default=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    status = models.BooleanField('是否显示', choices=((True, '是'), (False, '否')), default=True)
    tags = TaggableManager(blank=True)
    slug = models.SlugField(null=True, unique=True, blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def upload_docx(self):
        return format_html(
            '<div class="layui-upload-drag" id="upload_docx"><i class="layui-icon"></i><p>点击上传，或将文件拖拽到此处</p></div>')

    upload_docx.allow_tags = True
    upload_docx.short_description = '上传word文档'

    class Meta:
        db_table = 'at_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name + "管理"
        ordering = ['-id']

    def __str__(self):
        return self.title

    def increase_visit(self):
        self.visits += 1
        self.save()
        return self.visits

    # 获取文章地址
    # def get_absolute_url(self):
    #     return reverse('article:article_detail', args=[self.id])


class RemoteImages(models.Model):
    file_name = models.CharField('文件名称', max_length=255)
    origin_src = models.CharField('原始地址', max_length=255, db_index=True)
    local_src = models.CharField('本地地址', max_length=255, blank=True, null=True)
    remote_src = models.CharField('远程地址', max_length=255, blank=True, null=True, db_index=True)
    schema = models.IntegerField('URL类型', choices=((1, 'HTTPS'), (2, 'HTTP')), default=1)
    upload_from = models.IntegerField('添加来源', choices=((1, '自动抓取'), (2, '手动添加')), default=1)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'at_remote_images'
        verbose_name = '远程图片'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.file_name
