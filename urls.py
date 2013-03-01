from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('rownodzien',
    url(r'^$', 'main.views.main'),
    url(r'^book/add/$', 'books.form_book.add_book'),
    url(r'^book/(?P<isbn>\d+)/$', 'books.form_book.edit_book'),
    # Examples:
    # url(r'^$', 'rownodzien.views.home', name='home'),
    # url(r'^rownodzien/', include('rownodzien.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()