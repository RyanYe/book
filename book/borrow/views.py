# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from borrow.models import Book,Record
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout,hashers
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def record(request):
	sql = 'select a.* ,\
	 b.name as books, b.id as bookId from borrow_record \
	 as a , borrow_book as b  \
	 where a.book_id=b.id and a.user_id='
	sql +=str(request.user.id)+" order by borrow_date DESC"
	latest_record = Record.objects.raw(sql)
	return render_to_response('borrow/record.html',{"latest_record":latest_record},context_instance=RequestContext(request))


@login_required
def book(request,book_id):
	b = get_object_or_404(Book,pk=book_id)
	if b.status=="available":
		u = request.user
	else:
		sql = ' select * from borrow_record where book_id='+str(book_id)+' order by borrow_date DESC'
		borrow_date = Record.objects.raw(sql)[0]
		userId = borrow_date.user_id
		u = get_object_or_404(User,pk=userId)

	return render_to_response('borrow/book.html',{'book':b,'user':u},context_instance=RequestContext(request))


@login_required
def borrow(request,book_id):

	b = Book.objects.get(pk=book_id)
	b.status = "borrowed"
	b.save()

	u = request.user

	record = Record(book=b, user=u, borrow_date=timezone.now())
	record.save();
	return HttpResponseRedirect(reverse('borrow.views.book',args={b.id,}))
	

@login_required
def return_book(request,record_id):

	r = get_object_or_404(Record,pk=record_id)
	r.back_date = timezone.now()
	r.save()
	bookID = r.book_id
	book = get_object_or_404(Book,pk=bookID)
	book.status = "available"
	book.save()
	
	return HttpResponseRedirect(reverse('borrow.views.record'))

@login_required
def booklist(request):
	b = Book.objects.all()
	return render_to_response('borrow/book_list.html',{"book_list":b},context_instance=RequestContext(request))


def login_view(request):
	return render_to_response('borrow/login_view.html',context_instance=RequestContext(request))


# @login_required
def login_result(request):
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username=username,password=password)
	if user is not None:
		login(request,user)
		b = Book.objects.all()
		return render_to_response('borrow/book_list.html',{"book_list":b},context_instance=RequestContext(request))
	else:
		info = "wrong username or password"
		return render_to_response('borrow/login_view.html',{"info":info},context_instance=RequestContext(request))


@login_required
def logout_view(request):
	logout(request)
	return render_to_response('borrow/login_view.html',context_instance=RequestContext(request))
# 	return store_view(request)
# def user(request,user_id):
# 	u = get_object_or_404(User,pk=user_id)
# 	return render_to_response('borrow/index.html',{'user':u})


def regist(request):
	return render_to_response('borrow/regist.html', context_instance=RequestContext(request));



def regist_result(request):
	username=request.POST['username']
	try:
		user = User.objects.get(username__exact=username)
		return render_to_response('borrow/regist.html',{"info":"username already exists"}, context_instance=RequestContext(request))
		
	except:
		
		password1 = request.POST['password1']
		password2 = request.POST['password2']

		if password1 == password2 :
			user = User.objects.create_user(username=username,password=password1)
			user.is_staff = True
			user.save
			return render_to_response('borrow/login_view.html',context_instance=RequestContext(request))
		else :
			return render_to_response('borrow/regist.html',{"info":"passwords aren't match"}, context_instance=RequestContext(request))
