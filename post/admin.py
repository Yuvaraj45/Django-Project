from django.contrib import admin
from .models import post,profile,Images
# Register your models here.
class postadmin(admin.ModelAdmin):
	list_display = ('title','author','created','status')
	list_filter = ('title','author')
	search_fields = ('title__icontains',)
	# prepopulated_fields = {'slug':('title',)}
	list_editable = ('status',)

class profileadmin(admin.ModelAdmin):
	list_display = ('user','dob')

class Imagesadmin(admin.ModelAdmin):
	list_display = ('post','image')
	
admin.site.register(post,postadmin)
admin.site.register(profile,profileadmin)
admin.site.register(Images,Imagesadmin)
