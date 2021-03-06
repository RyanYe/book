from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'book.views.home', name='home'),
    # url(r'^book/', include('book.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$','borrow.views.booklist'),
    url(r'^accounts/login/$','borrow.views.login_view'),
    url(r'^accounts/logout/$','borrow.views.logout_view'),
    url(r'^borrow/',include('borrow.urls')),
    url(r'^admin/', include(admin.site.urls)),
 #    url(r'^accounts/login/$'),'borrow.login_view'),
	# url(r'^accounts/logout/$'),'borrow.logout_view'),
)
