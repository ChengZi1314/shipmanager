from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
import markdown2
from django.db import models
from .models import User, Library, Information, Article, Contact,PersonalCV
from django.views.generic.list import ListView
from .forms import BlogCommentForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView


def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


class Personal(ListView):
    template_name = "users/personal.html"
    context_object_name = "cv_list"

    def get_queryset(self):
        a_call_name = self.request.GET.get('insert_call_name')
        a_age = self.request.GET.get('insert_age')
        a_gender = self.request.GET.get('insert_gender')
        a_nation = self.request.GET.get('insert_nation')
        a_tall = self.request.GET.get('insert_tall')
        a_address = self.request.GET.get('insert_address')
        a_graduate = self.request.GET.get('insert_graduate')
        a_graduate_time = self.request.GET.get('insert_graduate_time')
        a_major = self.request.GET.get('insert_major')
        a_work_age = self.request.GET.get('insert_work_age')
        a_present_duty = self.request.GET.get('insert_present_duty')
        a_language = self.request.GET.get('insert_language')
        a_special_skills = self.request.GET.get('insert_special_skills')
        a_duty = self.request.GET.get('insert_duty')
        a_salary = self.request.GET.get('insert_salary')
        a_route_area = self.request.GET.get('insert_route_area')
        a_contract = self.request.GET.get('insert_contract')
        a_recruitment_ship = self.request.GET.get('insert_recruitment_ship')
        a_certificate_level = self.request.GET.get('insert_certificate_level')
        a_special_certificate = self.request.GET.get('insert_special_certificate')
        a_QQ = self.request.GET.get('insert_QQ')
        a_tel = self.request.GET.get('insert_tel')
        a_experience = self.request.GET.get('insert_experience')
        a_introduction = self.request.GET.get('insert_introduction')
        a_time = self.request.GET.get('insert_time')
        if a_call_name:
            if a_duty:
                if a_tel:
                    PersonalCV.objects.create(
                        call_name=a_call_name,
                        age=a_age,
                        gender=a_gender,
                        nation=a_nation,
                        tall=a_tall,
                        address=a_address,
                        graduate=a_graduate,
                        graduate_time=a_graduate_time,
                        major=a_major,
                        work_age=a_work_age,
                        present_duty=a_present_duty,
                        language=a_language,
                        special_skills=a_special_skills,
                        duty=a_duty,
                        salary=a_salary,
                        route_area=a_route_area,
                        contract=a_contract,
                        recruitment_ship=a_recruitment_ship,
                        certificate_level=a_certificate_level,
                        special_certificate=a_special_certificate,
                        QQ=a_QQ,
                        tel=a_tel,
                        experience=a_experience,
                        introduction=a_introduction,
                        time=a_time,
                    )
            cv_list = PersonalCV.objects.all()
        else:
            cv_list = PersonalCV.objects.all()
        return cv_list

    def get_context_data(self, **kwargs):
        return super(Personal, self).get_context_data(**kwargs)


class Search(ListView):
    template_name = "recruit/search.html"
    context_object_name = "recruit_list"

    def get_queryset(self):
        search_ship_age = self.request.GET.get('search_ship_age')
        search_duty = self.request.GET.get('search_duty')
        search_duty_id = self.request.GET.get('search_duty_id')
        search_company_name = self.request.GET.get('search_company_name')
        search_certificate_level = self.request.GET.get('search_certificate_level')
        search_special_certificate = self.request.GET.get('search_special_certificate')
        search_route_area = self.request.GET.get('search_route_area')
        search_recruitment_ship = self.request.GET.get('search_recruitment_ship')
        search_tonnage = self.request.GET.get('search_tonnage')
        search_time = self.request.GET.get('search_time')

        self.request.session["ship_age"] = search_ship_age
        self.request.session["duty"] = search_duty
        self.request.session["duty_id"] = search_duty_id
        self.request.session["company_name"] = search_company_name
        self.request.session["certificate_level"] = search_certificate_level
        self.request.session["special_certificate"] = search_special_certificate
        self.request.session["route_area"] = search_route_area
        self.request.session["recruitment_ship"] = search_recruitment_ship
        self.request.session["tonnage"] = search_tonnage
        self.request.session["time"] = search_time
        recruit_list = Library.objects.all()
        if search_ship_age:
            Information.objects.create(
                ship_age=search_ship_age,
                duty=search_duty,
                duty_id=search_duty_id,
                company_name=search_company_name,
                certificate_level=search_certificate_level,
                special_certificate=search_special_certificate,
                route_area=search_route_area,
                recruitment_ship=search_recruitment_ship,
                tonnage=search_tonnage,
                time=search_time,
            )
        else:
            return recruit_list

    def get_context_data(self, **kwargs):
        return super(Search, self).get_context_data(**kwargs)


class Search_Crew(ListView):
    template_name = "recruit/search_crew.html"
    context_object_name = "crew_list"

    def get_queryset(self):
        search_duty = self.request.GET.get('search_duty')
        search_certificate_level = self.request.GET.get('search_certificate_level')
        search_special_certificate = self.request.GET.get('search_special_certificate')
        search_route_area = self.request.GET.get('search_route_area')
        search_time = self.request.GET.get('search_time')

        self.request.session["duty"] = search_duty
        self.request.session["certificate_level"] = search_certificate_level
        self.request.session["special_certificate"] = search_special_certificate
        self.request.session["route_area"] = search_route_area
        self.request.session["time"] = search_time
        crew_list = PersonalCV.objects.all()

        return crew_list

    def get_context_data(self, **kwargs):
        return super(Search_Crew, self).get_context_data(**kwargs)


class Search_detail(ListView):
    template_name = "recruit/search_detail.html"
    context_object_name = "post_list"

    def get_queryset(self):

        search_ship_age = self.request.session.get('ship_age')
        search_duty = self.request.session.get('duty')
        search_company_name = self.request.session.get('company_name')
        search_certificate_level = self.request.session.get('certificate_level')
        search_special_certificate = self.request.session.get('special_certificate')
        search_route_area = self.request.session.get('route_area')
        search_recruitment_ship = self.request.session.get('recruitment_ship')
        search_tonnage = self.request.session.get('tonnage')
        search_time = self.request.session.get('time')

        if search_duty == '':
            post_list = Library.objects.all()
        else:
            post_list = Library.objects.filter(duty__exact=search_duty)
        if search_ship_age == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(ship_age__exact=search_ship_age)
        if search_company_name == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(company_name__iexact=search_company_name)
        if search_certificate_level == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(certificate_level__exact=search_certificate_level)
        if search_special_certificate == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(special_certificate__exact=search_special_certificate)
        if search_route_area == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(route_area__exact=search_route_area)
        if search_recruitment_ship == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(recruitment_ship__exact=search_recruitment_ship)
        if search_tonnage == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(tonnage__exact=search_tonnage)
        if search_time == '':
            post_list = post_list.filter()
        else:
            post_list = post_list.filter(time__exact=search_time)
        return post_list

    def get_context_data(self, **kwargs):
        return super(Search_detail, self).get_context_data(**kwargs)


class Crew_Detail(ListView):
    template_name = "recruit/crew_detail.html"
    context_object_name = "cv_list"

    def get_queryset(self):
        search_duty = self.request.session.get('duty')
        search_certificate_level = self.request.session.get('certificate_level')
        search_special_certificate = self.request.session.get('special_certificate')
        search_route_area = self.request.session.get('route_area')
        search_recruitment_ship = self.request.session.get('recruitment_ship')
        search_time = self.request.session.get('time')

        if search_duty == '':
            cv_list = PersonalCV.objects.all()
        else:
            cv_list = PersonalCV.objects.filter(duty__exact=search_duty)
        if search_certificate_level == '':
            cv_list = cv_list.filter()
        else:
            cv_list = cv_list.filter(certificate_level__exact=search_certificate_level)
        if search_special_certificate == '':
            cv_list = cv_list.filter()
        else:
            cv_list = cv_list.filter(special_certificate__exact=search_special_certificate)
        if search_route_area == '':
            cv_list = cv_list.filter()
        else:
            cv_list = cv_list.filter(route_area__exact=search_route_area)
        if search_recruitment_ship == '':
            cv_list = cv_list.filter()
        else:
            cv_list = cv_list.filter(recruitment_ship__exact=search_recruitment_ship)
        if search_time == '':
            cv_list = cv_list.filter()
        else:
            cv_list = cv_list.filter(time__exact=search_time)
        return cv_list

    def get_context_data(self, **kwargs):
        return super(Crew_Detail, self).get_context_data(**kwargs)


class News(ListView):
    template_name = "news/news_list.html"
    context_object_name = "article_list"

    def get_queryset(self):
        # 过滤数据，获取所有已发布文章，并且将内容转成markdown形式
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['body_archive'] = Article.objects.archive()
        return super(News, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "news/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'
    # pk_url_kwarg用于接受一个来自url中的主键，然后会根据这个主键进行查询
    # 我们之前在urlpatterns已经捕获article_id

    def get_object(self, queryset=None):
        # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
        # 返回该视图要显示的对象
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

    # 第五周新增
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class ArchiveView(ListView):
    template_name = "news/news_list.html"
    context_object_name = "article_list"

    def get_queryset(self):  # 接收从url传递的year和month参数，转为int类型
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])  # 按照year和month过滤文章
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        return super(ArchiveView, self).get_context_data(**kwargs)


# 第五周新增
class CommentPostView(FormView):
    form_class = BlogCommentForm
    template_name = 'news/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'news/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })


class Contacts(ListView):
    template_name = 'contact/contact.html'
    context_object_name = "con_list"

    def get_queryset(self):
        # 过滤数据，获取所有已发布文章，并且将内容转成markdown形式
        con_list = Contact.objects.all()
        return con_list

    def get_context_data(self, **kwargs):
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['body_archive'] = Article.objects.archive()
        return super(Contacts, self).get_context_data(**kwargs)


class Recruit(ListView):
    template_name = 'recruit/recruit.html'
    context_object_name = "library_list"

    def get_queryset(self):
        # 过滤数据，获取所有已发布文章，并且将内容转成markdown形式
        a_ship_age = self.request.GET.get('insert_ship_age')
        a_duty = self.request.GET.get('insert_duty')
        a_certificate_level = self.request.GET.get('insert_certificate_level')
        a_special_certificate = self.request.GET.get('insert_special_certificate')
        a_route_area = self.request.GET.get('insert_route_area')
        a_recruitment_ship = self.request.GET.get('insert_recruitment_ship')
        a_tonnage = self.request.GET.get('insert_tonnage')
        a_time = self.request.GET.get('insert_time')
        a_onboard_location = self.request.GET.get('insert_onboard_location')
        a_onboard_time = self.request.GET.get('insert_onboard_time')
        a_salary = self.request.GET.get('insert_salary')
        a_contract = self.request.GET.get('insert_contract')
        a_require = self.request.GET.get('insert_require')
        a_company_name = self.request.GET.get('insert_company_name')
        a_QQ = self.request.GET.get('insert_QQ')
        a_contact = self.request.GET.get('insert_contact')
        a_tel = self.request.GET.get('insert_tel')
        a_address = self.request.GET.get('insert_address')
        a_property = self.request.GET.get('insert_property')
        a_email = self.request.GET.get('insert_email')
        a_introduction = self.request.GET.get('insert_introduction')
        if a_duty:
            if a_company_name:
                if a_tel:
                    Library.objects.create(
                        ship_age=a_ship_age,
                        duty=a_duty,
                        certificate_level=a_certificate_level,
                        special_certificate=a_special_certificate,
                        route_area=a_route_area,
                        recruitment_ship=a_recruitment_ship,
                        tonnage=a_tonnage,
                        time=a_time,
                        onboard_location=a_onboard_location,
                        onboard_time=a_onboard_time,
                        salary=a_salary,
                        contract=a_contract,
                        require=a_require,
                        company_name=a_company_name,
                        QQ=a_QQ,
                        contact=a_contact,
                        tel=a_tel,
                        address=a_address,
                        property=a_property,
                        email=a_email,
                        introduction=a_introduction,
                    )
            library_list = Library.objects.all()
        else:
            library_list=Library.objects.all()
        return library_list

    def get_context_data(self, **kwargs):
        return super(Recruit, self).get_context_data(**kwargs)


class Company_Detail(DetailView):
    model = Library
    template_name = "recruit/company_detail.html"
    context_object_name = "recruit"
    pk_url_kwarg = 'library_id'

    # pk_url_kwarg用于接受一个来自url中的主键，然后会根据这个主键进行查询
    # 我们之前在urlpatterns已经捕获article_id

    def get_object(self, queryset=None):
        # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
        # 返回该视图要显示的对象

        obj = super(Company_Detail, self).get_object()
        return obj

    # 第五周新增
    def get_context_data(self, **kwargs):
        return super(Company_Detail, self).get_context_data(**kwargs)


class CV_Detail(DetailView):
    model = PersonalCV
    template_name = "recruit/cv_detail.html"
    context_object_name = "cv"
    pk_url_kwarg = 'cv_id'

    # pk_url_kwarg用于接受一个来自url中的主键，然后会根据这个主键进行查询
    # 我们之前在urlpatterns已经捕获article_id

    def get_object(self, queryset=None):
        # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
        # 返回该视图要显示的对象

        obj = super(CV_Detail, self).get_object()
        return obj

    # 第五周新增
    def get_context_data(self, **kwargs):
        return super(CV_Detail, self).get_context_data(**kwargs)


class PostArticle(ListView):
    template_name = "news/post_article.html"
    context_object_name = "post_article"

    def get_queryset(self):
        a_title = self.request.GET.get('insert_title')
        a_body = self.request.GET.get('insert_body')
        if a_title:
            if a_body:
                Article.objects.create(
                    title=a_title,
                    body=a_body,
                    status='p',
                )
        post_article = Article.objects.all()
        return post_article

    def get_context_data(self, **kwargs):
        return super(PostArticle, self).get_context_data(**kwargs)


class AddContact(ListView):
    template_name = "contact/add_contact.html"
    context_object_name = "contact_list"

    def get_queryset(self):
        a_name = self.request.GET.get('insert_name')
        a_QQ = self.request.GET.get('insert_QQ')
        a_email = self.request.GET.get('insert_email')
        a_tel = self.request.GET.get('insert_tel')
        a_duty = self.request.GET.get('insert_duty')
        a_company_name = self.request.GET.get('insert_company_name')
        if a_name:
            if a_duty:
                Contact.objects.create(
                    name=a_name,
                    QQ=a_QQ,
                    email=a_email,
                    tel=a_tel,
                    duty=a_duty,
                    company_name=a_company_name,
                )
        contact_list = Contact.objects.all()
        return contact_list

    def get_context_data(self, **kwargs):
        return super(AddContact, self).get_context_data(**kwargs)

"""
  def getuser(self, request):
        b_username = request.COOKIES.get('username')
        title_list = User.objects.filter(username__exact=b_username)[0:1]

        if request.method == 'POST':
            a_user = request.POST['user']
            a_call_name = request.POST['call_name']
            a_tel = request.POST['tel']
            a_work_age = request.POST['work_age']
            a_duty = request.POST['duty']
            a_certificate_level = request.POST['certificate_level']
            a_special_certificate = request.POST.get('special_certificate', False)
            a_route_area = request.POST.get('route_area', False)
            a_recruitment_ship = request.POST.get('recruitment_ship', False)
            a_post_time = request.POST.get('post_time', False)

            userinformation = User.objects.get(username=a_user)
            userinformation.call_name = a_call_name
            userinformation.work_age = a_work_age
            userinformation.tel = a_tel
            userinformation.duty = a_duty
            userinformation.certificate_level = a_certificate_level
            userinformation.special_certificate = a_special_certificate
            userinformation.route_area = a_route_area
            userinformation.recruitment_ship = a_recruitment_ship
            userinformation.post_time = a_post_time
            userinformation.save()

        return render_to_response('users/personal.html', {'title_list': title_list})
"""