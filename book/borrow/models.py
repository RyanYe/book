from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Book(models.Model):
	"""Book model"""
	STATUS = (
		(u'Available',u'Available'),
		(u'Borrowed',u'Borrowed'),
		)
	title = models.CharField(max_length=200,null=True,blank=True)
	ISBN = models.CharField(max_length=20)
	author = models.CharField(max_length=100,null=True,blank=True)
	status = models.CharField(max_length=20,choices=STATUS)
	img = models.CharField(max_length=200,null=True,blank=True)
	pages = models.CharField(max_length=10,null=True,blank=True)
	publisher = models.CharField(max_length=200,null=True,blank=True)
	summary = models.CharField(max_length=1000,null=True,blank=True)

	def __unicode__(self):
		return self.title

		
class Record(models.Model):
	"""Record Model"""
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	borrow_date = models.DateTimeField()
	back_date = models.DateTimeField(null=True)

	def __unicode__(self):
		b = Book.objects.get(id=self.book_id);
		return b.name
		
	def borrow(book_id, user_id):
		b = Book.objects.get(pk=book_id)
		b.status = "borrowed"
		b.save()

		u = User.objects.get(pk=user_id)

		record = Record(book=b, user=u, borrow_date=timezone.now())
		record.save();
		
	def give_back(record_id):
		r = Record.objects.get(pk=record_id);
		b = r.book
		b.status = "available"
		b.save()

		r.back_date = timezone.now()
		r.save()
		