# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from borrow.models import Book,User,Record
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
import datetime
from django.utils import timezone

def record(request):
	latest_record = Record.objects.raw('select a.* ,\
	 u.name as users, b.name as books from borrow_record \
	 as a left join borrow_book as b left join borrow_user \
	 as u where a.book_id=b.id and a.user_id=u.id'
	 )
	return render_to_response('borrow/record.html',{"latest_record":latest_record})

def book(request,book_id):
	b = get_object_or_404(Book,pk=book_id)
	u = get_object_or_404(User,username="yuye")
	return render_to_response('borrow/book.html',{'book':b,'user':u},context_instance=RequestContext(request))

def borrow(request,book_id):

	b = Book.objects.get(pk=book_id)
	b.status = "borrowed"
	b.save()

	username="yuye"
	u = User.objects.get(username__exact=username)

	record = Record(book=b, user=u, borrow_date=timezone.now())
	record.save();
	return HttpResponseRedirect(reverse('borrow.views.book',args={b.id,}))

# def user(request,user_id):
# 	u = get_object_or_404(User,pk=username)
# 	return render_to_response('borrow/user.html',{'user':u},context_instance=RequestContext(request))
def booklist(request):
	b = Book.objects.all()
	return render_to_response('borrow/book_list.html',{"book_list":b})
# def login_view(request):
# 	user = authenticate(username=request.POST['username'],passowrd=request.POST['passowrd'])
# 	if user is not None:
# 		login(request,user)
# 		print request.user
# 		return list_product(request)
# 	else:
# 		return store_view(request)

# def logout_view(request):
# 	logout(request)
# 	return store_view(request)
#def user(request,user_id):
#	u = get_object_or_404(User,pk=user_id)
#	return render_to_response('borrow/index.html',{'user':u})