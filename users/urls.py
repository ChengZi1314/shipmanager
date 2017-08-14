from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^$', views.Search.as_view(), name='search'),
    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^search_detail/$', views.Search_detail.as_view(), name='search_detail'),
    url(r'^news/$', views.News.as_view(), name='News'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    url(r'^personal/$', views.Personal.as_view(), name='personal'),
    url(r'^contact/$', views.Contacts.as_view(), name='contact'),
    url(r'^recruit/$',views.Recruit.as_view(), name='recruit'),
    url(r'^library/(?P<library_id>\d+)$', views.Company_Detail.as_view(), name='company_detail'),
    url(r'^search_crew/$', views.Search_Crew.as_view(), name='search_crew'),
    url(r'^crew_detail/$', views.Crew_Detail.as_view(), name='crew_detail'),
    url(r'^cv/(?P<cv_id>\d+)$', views.CV_Detail.as_view(), name='cv_detail'),
    url(r'^post_article/$', views.PostArticle.as_view(), name='post_article'),
    url(r'^add_contact/$', views.AddContact.as_view(), name='add_contact'),
]