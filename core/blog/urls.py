from django.urls import path
from .views import *
from blog.feeds import LatestEntriesFeed
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
app_name  = 'blog'

urlpatterns = [
    path ('', indexView, name='fbv-index'),
    # path ('about/', TemplateView.as_view(template_name='about.html',extra_context={"name": "alias"}),
    path ('cbv-index/', IndexView.as_view(), name='cbv-index' ),
    path ('go-to-index/', RedirectView.as_view(pattern_name="blog:cbv-index"), name='redirect-to-index' ),
    path ('post/', PostList.as_view(), name='post-list' ),
    # path('' , blog_view, name='index'),
    # path('<int:pid>', blog_single_view, name='single'),
    # path('category/<str:cat_name>' , blog_view, name='category'),
    # path('tag/<str:tag_name>' , blog_view, name='tag'),
    # path('author/<str:author_username>' , blog_view, name='author'),
    # path('search/', blog_search, name='search'),
    # path('rss/feed/', LatestEntriesFeed()),
]