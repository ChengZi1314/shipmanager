from django.db import models
from django.contrib import admin
from collections import defaultdict
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField('昵称',max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass
admin.site.register(User)


class PersonalCV(models.Model):

    call_name = models.CharField('称呼', max_length=200, null=True)
    age = models.CharField('年龄', max_length=200, null=True)
    gender = models.CharField('性别', max_length=200, null=True)
    nation = models.CharField('民族', max_length=200, null=True)
    tall = models.CharField('身高', max_length=200, null=True)
    native = models.CharField('籍贯', max_length=200, null=True)
    address = models.CharField('现地址', max_length=200, null=True)
    graduate = models.CharField('毕业院校', max_length=200, null=True)
    graduate_time = models.CharField('毕业时间', max_length=200, null=True)
    major = models.CharField('专业', max_length=200, null=True)
    certificate_level = models.CharField('证书等级', max_length=200, null=True)
    work_age = models.CharField('工作时间', max_length=200, null=True)
    present_duty = models.CharField('现职位', max_length=200, null=True)
    language = models.CharField('外语', max_length=200, null=True)
    special_skills = models.CharField('特殊技能', max_length=2000, null=True)
    duty = models.CharField('求职职位', max_length=200, null=True)
    salary = models.CharField('月薪', max_length=200, null=True)
    route_area = models.CharField('航线区域', max_length=200, null=True)
    contract = models.CharField('合同年限', max_length=200, null=True)
    recruitment_ship = models.CharField('招聘船型', max_length=200, null=True)
    special_certificate = models.CharField('特殊证书', max_length=200, null=True)
    post_time = models.DateField('发布时间', max_length=200, null=True, auto_now_add=True)
    tel = models.CharField('电话', max_length=200, null=True)
    QQ = models.CharField('QQ', max_length=200, null=True)
    experience = models.TextField('工作经历', max_length=200, null=True)
    introduction = models.TextField('自我介绍', max_length=200, null=True)
    time = models.CharField('时间范围', max_length=30, null=True)

    class Meta:
        # mata包含一系列选项
        ordering = ['-post_time']

    def get_absolute_url(self):
        return reverse('users:cv_detail', kwargs={'cv_id': self.pk})
admin.site.register(PersonalCV)


class Library(models.Model):

    duty = models.CharField(max_length=70, null=True)
    duty_id = models.CharField('职务编号',max_length=20, null=True)
    ship_age = models.CharField('船龄',max_length=10, null=True)
    company_name = models.CharField('公司名称', max_length=300, null=True)
    certificate_level = models.CharField('证书等级', max_length=200, null=True)
    special_certificate = models.CharField('特殊证书', max_length=300, null=True)
    route_area = models.CharField('路线区域', max_length=300, null=True)
    recruitment_ship = models.CharField('招聘船型', max_length=300, null=True)
    tonnage = models.CharField('吨位', max_length=200, null=True)
    post_time = models.DateField('搜索时间', max_length=300, null=True, auto_now=True)
    time = models.CharField('搜索时间', max_length=300, null=True)
    onboard_location = models.CharField('上船地点', max_length=300, null=True)
    onboard_time = models.CharField('上船时间', max_length=200, null=True)
    salary = models.CharField('提供月薪', max_length=300, null=True)
    contract = models.CharField('合同年限', max_length=300, null=True)
    require = models.TextField('具体要求', max_length=300, null=True)
    QQ = models.CharField('在线QQ', max_length=300, null=True)
    contact = models.CharField('联系人', max_length=300, null=True)
    tel = models.CharField('公司电话', max_length=300, null=True)
    address = models.CharField('公司地址', max_length=300, null=True)
    property = models.CharField('公司性质', max_length=200, null=True)
    email = models.CharField('电子邮箱', max_length=300, null=True)
    introduction = models.TextField('公司介绍', max_length=300, null=True)

    class Meta:
        # mata包含一系列选项
        ordering = ['-post_time']

    def get_absolute_url(self):
        return reverse('users:company_detail', kwargs={'library_id': self.pk})

admin.site.register(Library)


class Information(models.Model):
    duty = models.CharField('职务', max_length=200, null=True)
    duty_id = models.CharField('职位编号', max_length=300, null=True)
    ship_age = models.CharField('船龄', max_length=100, null=True)
    company_name = models.CharField('公司名称', max_length=300, null=True)
    certificate_level = models.CharField('职务', max_length=200, null=True)
    special_certificate = models.CharField('特殊证书', max_length=300, null=True)
    route_area = models.CharField('路线区域', max_length=300, null=True)
    recruitment_ship = models.CharField('招聘船型', max_length=300, null=True)
    tonnage = models.CharField('吨位', max_length=200, null=True)
    time = models.CharField('搜索时间', max_length=30, null=True)

    def __str__(self):
        return self.duty

admin.site.register(Information)


class ArticleManage(models.Manager):
    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)
                # 模板不支持defaultdict


class Article(models.Model):

    objects = ArticleManage()
    title = models.CharField('标题', max_length=70)
    body = models.TextField(' 正文')
    created_time = models.DateTimeField('创建时间', null=True, auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间',auto_now_add=True)
    status = models.CharField('文章状态', max_length=1)
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True, help_text="可选，如若为空将摘取正文的前54个字符")

    def __str__(self):
        # 主要用于交互解释器显示表示该类的字符串
        # self代表调用该函数对象本身
        return self.title

    class Meta:
        # mata包含一系列选项
        ordering = ['-last_modified_time']
        # ordering表示排序，-表示逆序，是按照时间逆序排列的

    # 第五周：新增 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'article_id': self.pk})

admin.site.register(Article)


class BlogComment(models.Model):
    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]


class Contact(models.Model):
    name = models.CharField('姓名', max_length=30, null=True)
    QQ = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=30, null=True)
    tel = models.CharField(max_length=20, null=True)
    duty = models.CharField('职务', max_length=200, null=True)
    company_name = models.CharField('公司名称', max_length=300, null=True)

    def __str__(self):
        return self.name
admin.site.register(Contact)


"""
duty_choice = (('', '---其他---'),
               ('整套班子', '整套班子'),
               ('船长', '船长'),
               ('大副', '大副'),
               ('二副', '二副'),
               ('三副', '三副'),
               ('白皮三副', '白皮三副'),
               ('驾助', '驾助'),
               ('实习三副', '实习三副'),
               ('GMDSS普通操作员', 'GMDSS普通操作员'),
               ('水手长', '水手长'),
               ('木匠', '木匠'),
               ('水手', '水手'),
               ('高级水手', '高级水手'),
               ('二水', '二水'),
               ('新证水手', '新证水手'),
               ('实习水手', '实习水手'),
               ('轮机长', '轮机长'),
               ('大管轮', '大管轮'),
               ('二管轮', '二管轮'),
               ('三管轮', '三管轮'),
               ('白皮三管', '白皮三管'),
               ('电机员', '电机员'),
               ('电工', '电工'),
               ('轮助', '轮助'),
               ('实习三管', '实习三管'),
               ('机工长', '机工长'),
               ('铜匠', '铜匠'),
               ('泵匠', '泵匠'),
               ('机工', '机工'),
               ('高级机工', '高级机工'),
               ('新证机工', '新证机工'),
               ('实习机工', '实习机工'),
               ('高级水手', '高级水手'),
               ('大厨', '大厨'),
               ('服务员', '服务员'),
               ('船医', '船医'),)
certificate_level_choice = (('', '---其他---'),
                            ('甲类', '甲类'),
                            ('乙一', '乙一'),
                            ('乙二', '乙二'),
                            ('丙一', '丙一'),
                            ('丙二', '丙二'),
                            ('丁类', '丁类'),
                            ('长一', '长一'),
                            ('长二', '长二'),
                            ('内河', '内河'),)
special_certificate_choice = (('', '---其他---'),
                              ('化高证书', '化高证书'),
                              ('油高证书', '油高证书'),
                              ('液高证书', '液高证书'),
                              ('油化双证', '油化双证'),
                              ('客滚船证书', '客滚船证书'),
                              ('海进江证书', '海进江证书'),
                              ('外籍签注适任证书', '外籍签注适任证书'),
                              ('高速船证书', '高速船证书'),)
route_area_choice = (('', '---其他---'),
                     ('中日韩', '中日韩'),
                     ('东南亚', '东南亚'),
                     ('中东波斯湾', '中东波斯湾'),
                     ('地中海', '地中海'),
                     ('南北美', '南北美'),
                     ('环球航线', '环球航线'),
                     ('内河航线', '内河航线'),
                     ('江海航线', '江海航线'),
                     ('长江航线', '长江航线'),)
recruit_ship_choice = (('', '---其他---'),
                       ('散杂货船', '散杂货船'),
                       ('集装箱船', '集装箱船'),
                       ('多用途船', '多用途船'),
                       ('油轮', '油轮'),
                       ('化学品船', '化学品船'),
                       ('油化船', '油化船'),
                       ('液化气船', '液化气船'),
                       ('工程船', '工程船'),
                       ('冷藏船', '冷藏船'),
                       ('港作船', '港作船'),
                       ('LNG动力船', 'LNG动力船'),
                       ('客船', '客船'),
                       ('客滚船', '客滚船'),
                       ('滚装汽车船', '滚装汽车船'),
                       ('拖轮', '拖轮'),
                       ('作业渔船', '作业渔船'),
                       ('打桩船', '打桩船'),
                       ('邮船', '邮船'),
                       ('沥青船', '沥青船'),
                       ('木材船', '木材船'),
                       ('泵船', '泵船'),
                       ('工作船', '工作船'),
                       ('邮政船', '邮政船'),
                       ('海监船', '海监船'),
                       ('救援船', '救援船'),
                       ('不上船', '不上船'),)
tonnage_choice = (('', '---其他---'),
                  ('5千吨以下', '5千吨以下'),
                  ('5千吨-1万吨', '5千吨-1万吨'),
                  ('1万吨-2万吨', '1万吨-2万吨'),
                  ('2万吨-3万吨', '2万吨-3万吨'),
                  ('3万吨-6万吨', '3万吨-6万吨'),
                  ('6万吨-10万吨', '6万吨-10万吨'),
                  ('10万吨-15万吨', '10万吨-15万吨'),
                  ('15万吨-30万吨', '15万吨-30万吨'),
                  ('30万吨以上', '30万吨以上'),)
time_choice = (('', '---其他---'),
               ('一星期内', '一星期内'),
               ('一个月内', '一个月内'),
               ('三个月内', '三个月内'),
               ('一年以内', '一年以内'),)
"""