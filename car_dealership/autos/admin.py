from django.contrib import admin
from .models import Car, Article, ContactMessage, Category, Car360Image

class Car360ImageInline(admin.TabularInline):
    model = Car360Image
    extra = 1  # Número de formularios vacíos a mostrar
    fields = ['image', 'angle']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'category')
    list_filter = ('brand', 'year', 'category')
    search_fields = ('brand', 'model', 'description')
    inlines = [Car360ImageInline]
    fieldsets = (
        ('Información Principal', {
            'fields': ('brand', 'model', 'year', 'price', 'category')
        }),
        ('Imágenes', {
            'fields': ('image', 'featured_image', 'image_url'),
        }),
        ('Detalles', {
            'fields': ('description', 'featured'),
        }),
    )

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
    fields = ('title', 'category', 'content', 'image_url')
    autocomplete_fields = ['category']

