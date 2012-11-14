from borrow.models import Book, User, Record
from django.contrib import admin
class BookAdmin(admin.ModelAdmin):
	fieldsets = [ 
		( None,		{'fields':['name']}),
		('Detail Info',{'fields':['ISBN','author']}),
		('Status',{'fields':['status']}),
	]
	search_fields = ['name','ISBN']
	list_display = ('name','ISBN','status')

class UserAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 		{'fields':['name']}),
		('Detail Info',{'fields':['password']}),
	]
	search_fields = ['name']

class RecordAdmin(admin.ModelAdmin):
	fields = ['book','user','borrow_date','back_date']
	list_display = ('id','book','user','borrow_date','back_date')
		
admin.site.register(Book, BookAdmin)
# admin.site.register(User, UserAdmin)
admin.site.register(Record,RecordAdmin)