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

    url(r'^reader/add/$', 'people.readers.add_reader'),
    url(r'^reader/(?P<number>\d+)/delete/$', 'people.readers.delete_reader'),
    url(r'^reader/(?P<number>\d+)/$', 'people.readers.edit_reader'),

    url(r'^librarian/add/$', 'people.librarians.add_librarian'),
    url(r'^librarian/(?P<number>\d+)/delete/$', 'people.librarians.delete_librarian'),
    url(r'^librarian/(?P<number>\d+)/$', 'people.librarians.edit_librarian'),

    url(r'^register/(?P<code>\d+)/$', 'rentings.views.register_rent'),
    url(r'^return/(?P<code>\d+)/$', 'rentings.views.register_return'),

    
    url(r'^reports/books/', 'reports.views.report_books'),
    url(r'^reports/instances/', 'reports.views.report_instances'),
    url(r'^reports/rentings/', 'reports.views.report_rentings'),
    url(r'^reports/rentings_history/', 'reports.views.report_rentingshistory'),
    url(r'^reports/readers/', 'reports.views.report_readers'),
    url(r'^reports/return_by_reader/(?P<pesel>\d+)/$','reports.views.report_returnbyreader'),
    url(r'^reports/ava_instances/(?P<isbn>\d+)/$','reports.views.report_avainstances'),
)

urlpatterns += staticfiles_urlpatterns()