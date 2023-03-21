from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import User, product_details,Comment_product,Bid

# Register your models here.
class productAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

admin.site.register(product_details,productAdmin) 
admin.site.register(Comment_product)
admin.site.register(Bid)
admin.site.register(User)