from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from borrow.models import Book, User, Record

urlpatterns = patterns('',
	url(r'^$','borrow.views.booklist'),
  url(r'^record/$','borrow.views.record'),
  url(r'^book/(?P<book_id>\d+)/borrow/$',"borrow.views.borrow"),
	url(r'^book/(?P<book_id>\d+)/$','borrow.views.book'),
  url(r'^user/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=User,
            template_name='borrow/user.html')),
   # url(r'^(?P<pk>\d+)/results/$',
   #     DetailView.as_view(
   #         model=User,
   #         template_name='borrow/user.html')),
   # url(r'^(?P<poll_id>\d+)/borrow/$', 'borrow.views.borrow'),
)