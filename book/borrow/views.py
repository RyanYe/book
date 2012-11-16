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
import json
import urllib
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
def user(request,user_id):
	u = get_object_or_404(User,pk=user_id)
	return render_to_response('borrow/user.html',{'user':u})


@login_required
def book(request,book_id):
	b = get_object_or_404(Book,pk=book_id)
	isbn = b.ISBN
	authors = b.author
	summary = b.summary
	summarylist = summary.split('\r\n')
	title = b.title
	img = b.img
	pages = b.pages
	publisher = b.publisher

	if b.status=="Available":
		u = request.user
	else:
		sql = ' select * from borrow_record where book_id='+str(book_id)+' order by borrow_date DESC'
		borrow_date = Record.objects.raw(sql)[0]
		userId = borrow_date.user_id
		u = get_object_or_404(User,pk=userId)

	return render_to_response('borrow/book.html',{'book':b,'user':u,"authors":authors,"summarylist":summarylist,"title":title,"img":img,"pages":pages,'publisher':publisher},context_instance=RequestContext(request))
	# return render_to_response('borrow/book.html',{'book':b,'user':u,"author":data},context_instance=RequestContext(request))

@login_required
def borrow(request,book_id):

	b = Book.objects.get(pk=book_id)
	b.status = "Borrowed"
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
	book.status = "Available"
	book.save()
	
	return HttpResponseRedirect(reverse('borrow.views.record'))

@login_required
def booklist(request):
	b = Book.objects.all()
	for book in b:
		download(book.id)

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


def download(pk):
	sql = "select * from borrow_book where id="+str(pk)
	books = Book.objects.raw(sql)
	for book in books:
		if book.title is None or book.title=="":
			isbn = book.ISBN

			url = 'http://api.douban.com/v2/book/isbn/'+isbn
			page = urllib.urlopen(url)
			data = page.read()
			ddata = json.read(data)
			book.author = ddata['author']
			book.summary = ddata['summary']
			book.title = ddata['title']
			book.img = ddata['images']['large']
			book.pages = ddata['pages']
			book.publisher = ddata['publisher']

			book.save()
