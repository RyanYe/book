import sys
sys.path.append('..')
sys.path.append('../..')
from django import template
from django.conf import settings
settings.configure()

from django.http import HttpResponse, HttpResponseRedirect
from borrow.models import Book
import json
import urllib

def download():
	sql = "select name, isbn from borrow_book"
	books = Book.objects.raw(sql)
	for book in books:
		if book.name is None:
			isbn = book.ISBN

			url = 'http://api.douban.com/v2/book/isbn/'+isbn
			page = urllib.urlopen(url)
			data = page.read()
			ddata = json.read(data)
			book.author = ddata['author'][0]
			book.summary = ddata['summary']
			book.title = ddata['title']
			book.img = ddata['images']['large']
			book.pages = ddata['pages']
			book.publisher = ddata['publisher']

			book.save()


download()