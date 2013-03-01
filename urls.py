from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('rownodzien',
    url(r'^$', 'main.views.main'),
    url(r'^book/add/$', 'books.books.add_book'),
    url(r'^book/(?P<isbn>\d+)/delete/$', 'books.books.delete_book'),
    url(r'^book/(?P<isbn>\d+)/$', 'books.books.edit_book'),

)

urlpatterns += staticfiles_urlpatterns()