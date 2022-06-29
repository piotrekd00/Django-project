from django.contrib import admin
from .models import RentalOffice, Book, Film, CD
# Register your models here.

admin.site.register(RentalOffice)
admin.site.register(Book)
admin.site.register(Film)
admin.site.register(CD)
