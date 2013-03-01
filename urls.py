from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('rownodzien',
    url(r'^$', 'main.views.main'),
    url(r'^book/add/$', 'books.books.add_book'),
    url(r'^book/(?P<isbn>\d+)/delete/$', 'books.books.delete_book'),
    url(r'^book/(?P<isbn>\d+)/add_instance/$', 'books.instances.add_instance'),
    url(r'^book/(?P<isbn>\d+)/$', 'books.books.edit_book'),
    url(r'^instance/(?P<code>\d+)/delete/$', 'books.instances.delete_instance'),
    url(r'^instance/(?P<code>\d+)/$', 'books.instances.edit_instance'),

)

urlpatterns += staticfiles_urlpatterns()