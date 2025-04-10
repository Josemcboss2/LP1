from django.contrib import admin
from .models import Car, Article, ContactMessage, Category

admin.site.register(Car)
admin.site.register(ContactMessage)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    fields = ('title', 'category', 'content', 'image_url')  # Define el orden de los campos en el formulario
    autocomplete_fields = ['category']  # Permite autocompletar la categoría

    