from django.db import models
import datetime
from django.utils import timezone

class Book(models.Model):
	"""Book model"""
	name = models.CharField(max_length=200)
	ISBN = models.CharField(max_length=20)
	author = models.CharField(max_length=100)
	status = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name



class User(models.Model):
	"""User Model"""
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name
		
class Record(models.Model):
	"""Record Model"""
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	borrow_date = models.DateTimeField()
	back_date = models.DateTimeField(null="true")

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
		