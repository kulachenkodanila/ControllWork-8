from django.contrib import admin

from webapp.models import Product, Review


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description', 'image']
    list_filter = ['category', 'name']
    search_fields = ['name', 'category', 'description']
    fields = ['name', 'category', 'description', 'image']
    # readonly_fields = ['updated_at', 'created_at']


admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'product', 'text', 'mark', 'moderated', 'created_at', 'updated_at']
    list_filter = ['author', 'product']
    search_fields = ['author', 'product']
    fields = ['author', 'product', 'text', 'mark', 'moderated']
    readonly_fields = ['updated_at', 'created_at']


admin.site.register(Review, ReviewAdmin)
