from django.contrib import admin
from core.pos.models import *


class AtributoProductInline(admin.TabularInline):
    model = AtributoProduct
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('Atributo', 'Costo',)
        }),
    )


class ProductoAdmin(admin.ModelAdmin):
    inlines = [AtributoProductInline]


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductoAdmin)
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(AtributoProduct)
