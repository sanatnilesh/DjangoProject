from django.contrib import admin
from django.db.models import Count, F, Value
from .models import Product, Category, Client, Order


@admin.action(description='add 50 value to the current stock of the item.')
def add_value(modeladmin, request, queryset):
    queryset.update(stock=F('stock')+50)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [add_value]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city')
    list_filter = ['interested_in']


# admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
