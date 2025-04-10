from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Car360Image(models.Model):
    car = models.ForeignKey('Car', related_name='images_360', on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='cars/360/',
                              processors=[ResizeToFit(1024, 1024)],
                              format='JPEG',
                              options={'quality': 85})
    angle = models.IntegerField(help_text="Ángulo de la imagen (0-359)")

    class Meta:
        ordering = ['angle']

class Car(models.Model):
    CATEGORY_CHOICES = [
        ('sedan', 'Sedán'),
        ('suv', 'SUV'),
        ('sports', 'Deportivo'),
        ('pickup', 'Pickup')
    ]
    
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    featured = models.BooleanField(default=False)  # New field
    image = ProcessedImageField(upload_to='cars/',
                              processors=[ResizeToFit(1200, 800)],
                              format='JPEG',
                              options={'quality': 85},
                              null=True,
                              blank=True)
    featured_image = ProcessedImageField(upload_to='cars/featured/',
                                       processors=[ResizeToFit(2048, 1365)],
                                       format='JPEG',
                                       options={'quality': 90},
                                       null=True,
                                       blank=True)
    
    @property
    def has_360_view(self):
        return self.images_360.exists()

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('contacted', 'Contactado'),
        ('resolved', 'Resuelto'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Mensaje de {self.name}"
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.name} en {self.article.title}"
    


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email