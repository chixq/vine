from django.conf.urls import patterns, include, url

from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from d1.views import *
from testapp.views import *
from vine_comment.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^comment/((?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)$', comment_board),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^write/(\w{1,40})$', comment_board),
    (r'^test/(\w+)$', get_comment_board_template),
    #(r'^test/', test_func),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #{'document_root': settings.STATIC_ROOT}),
    # Examples:
    # url(r'^$', 'd1.views.home', name='home'),
    # url(r'^d1/', include('d1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
    url(r'^articles/comments/', include('django.contrib.comments.urls')),
)

urlpatterns += patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),
)

urlpatterns += patterns('',
    (r'^about/', TemplateView.as_view(template_name="about.html")),
)

urlpatterns += patterns('',
    (r'^articles/(\d{4})/$', 'news.views.year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'news.views.month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'news.views.article_detail'),
)

urlpatterns += patterns('',
    url(r'^mine/$', MyView.as_view(), name='my-view'),
)

from feeds.views import LatestEntriesFeed
urlpatterns += patterns('',
    # ...
    (r'^latest/feed/$', LatestEntriesFeed()),
    # ...
)

urlpatterns += patterns('',
    url(r"comment_test/(?P<url_b64>.*?)/?$",
        CommentView.as_view(),
        name="comment")
)

urlpatterns += patterns('',
    url(r'testapp/(?P<para1>.*?)/(?P<para2>.*?)/(?P<comment_id>.*?)/$',
        TestAppView.as_view(),
        name='test_app'),
)

from functools import wraps
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static
from django.conf.urls import patterns, url

if settings.DEBUG:

    def custom_headers(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            response['Access-Control-Allow-Origin'] = '*'
            response['Custom-header'] = 'Awesome'
            response['Another-header'] = 'Bad ass'
            return response

        return wrapper

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', custom_headers(serve_static)),
    )
    