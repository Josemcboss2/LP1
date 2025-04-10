from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.utils import timezone
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.views.decorators.cache import cache_page
from imagekit.utils import get_cache
from datetime import datetime, timedelta
import json
from .models import Car, Article, ContactMessage, Category, Car360Image
from .forms import ContactForm
from .models import Article, Comment
from .models import Subscriber
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from .forms import ContactForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import caches

def home(request):
    # Get featured cars directly
    featured_cars = Car.objects.filter(featured=True)[:3]
    latest_articles = Article.objects.order_by('-created_at')[:5]
    
    context = {
        'featured_cars': featured_cars,
        'latest_articles': latest_articles,
    }
    return render(request, 'home.html', context)

def cars(request):
    # Obtener todos los carros inicialmente
    cars_list = Car.objects.all()
    
    # Filtrar por categoría
    category = request.GET.get('category')
    if category:
        cars_list = cars_list.filter(category=category)
    
    # Filtrar por marca
    brand = request.GET.get('brand')
    if brand:
        cars_list = cars_list.filter(brand=brand)
    
    # Filtrar por año
    year = request.GET.get('year')
    if year:
        cars_list = cars_list.filter(year=year)
    
    # Filtrar por precio máximo
    max_price = request.GET.get('max_price')
    if max_price:
        cars_list = cars_list.filter(price__lte=max_price)
    
    # Ordenar resultados
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_asc':
            cars_list = cars_list.order_by('price')
        elif sort == 'price_desc':
            cars_list = cars_list.order_by('-price')
        elif sort == 'year_desc':
            cars_list = cars_list.order_by('-year')
    
    # Obtener años únicos para el filtro
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Obtener marcas únicas para el filtro
    brands = Car.objects.values('brand').distinct().order_by('brand')
    
    context = {
        'cars': cars_list,
        'years': years,
        'brands': brands,
        'selected_category': category,
        'selected_year': year,
        'selected_brand': brand,
        'max_price': max_price
    }
    
    return render(request, 'cars.html', context)

@cache_page(60 * 15)  # Cache por 15 minutos
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    related_cars = Car.objects.filter(category=car.category).exclude(id=car_id)[:3]
    
    # Optimizar carga de imágenes 360°
    if car.has_360_view:
        images_360 = car.images_360.all()
        images_360_data = []
        for img in images_360:
            images_360_data.append({
                'image': request.build_absolute_uri(img.image.url),
                'angle': img.angle
            })
    else:
        images_360_data = []
    
    context = {
        'car': car,
        'related_cars': related_cars,
        'images_360': json.dumps(images_360_data)
    }
    
    return render(request, 'car_detail.html', context)

def articles(request):
    articles_list = Article.objects.all()
    categories = Category.objects.all()
    
    # Filtrar por categoría
    category = request.GET.get('category')
    if category:
        articles_list = articles_list.filter(category__slug=category)
    
    context = {
        'articles': articles_list,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'articles.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all().order_by('-created_at')
    comments_count = comments.count()
    
    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'comments_count': comments_count,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Procesa el formulario (envía el email, etc.)
            name = form.cleaned_data['name']
            
            # Si es una petición AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'¡Gracias {name}! Tu mensaje ha sido enviado.'
                })
            else:
                return HttpResponse('¡Mensaje enviado!')
        
        # Si hay errores
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors.items())
            }, status=400)
    
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def privacy(request):
    return render(request, 'privacy.html')

def car_inquiry(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        car = get_object_or_404(Car, id=car_id)

        # Crear el contenido del correo
        subject = f"Consulta sobre el vehículo: {car.year} {car.brand} {car.model}"
        body = (
            f"Nombre: {name}\n"
            f"Correo: {email}\n"
            f"Teléfono: {phone}\n\n"
            f"Mensaje:\n{message}"
        )

        # Configurar el correo con codificación UTF-8
        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email='joseanibalmencia@gmail.com',  # Cambia esto por tu correo
            to=['destinatario@example.com'],    # 
        )
        email_message.encoding = 'utf-8'  # Asegúrate de usar UTF-8

        try:
            email_message.send()
            messages.success(request, '¡Tu consulta ha sido enviada con éxito!')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {e}')

        return redirect('cars')

    return redirect('home')

def article_comment(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')

        # Guarda el comentario en la base de datos
        Comment.objects.create(
            article=article,
            name=name,
            email=email,
            comment=comment_text
        )

        messages.success(request, 'Tu comentario ha sido enviado. ¡Gracias!')
        return redirect('article_detail', article_id=article_id)
    else:
        return redirect('home')

    
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            Subscriber.objects.create(email=email)
            messages.success(request, '¡Gracias por suscribirte!')
        except:
            messages.error(request, 'Este correo ya está suscrito.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Estadísticas básicas
    total_cars = Car.objects.count()
    total_articles = Article.objects.count()
    total_subscribers = Subscriber.objects.count()
    
    # Consultas del mes actual
    now = timezone.now()
    first_day = now.replace(day=1, hour=0, minute=0, second=0)
    monthly_inquiries = ContactMessage.objects.filter(created_at__gte=first_day).count()
    
    # Datos para el gráfico de consultas por mes
    last_6_months = []
    monthly_inquiries_data = []
    for i in range(5, -1, -1):
        date = now - timedelta(days=30*i)
        month_start = date.replace(day=1, hour=0, minute=0, second=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        count = ContactMessage.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()
        last_6_months.append(date.strftime('%B'))
        monthly_inquiries_data.append(count)
    
    # Datos para el gráfico de categorías
    categories = Car.objects.values('category').annotate(count=Count('id'))
    category_labels = [dict(Car.CATEGORY_CHOICES)[cat['category']] for cat in categories]
    category_data = [cat['count'] for cat in categories]
    
    # Últimas consultas
    recent_inquiries = ContactMessage.objects.select_related('car').order_by('-created_at')[:10]
    
    context = {
        'total_cars': total_cars,
        'total_articles': total_articles,
        'total_subscribers': total_subscribers,
        'monthly_inquiries': monthly_inquiries,
        'months_labels': json.dumps(last_6_months),
        'monthly_inquiries_data': monthly_inquiries_data,
        'category_labels': json.dumps(category_labels),
        'category_data': category_data,
        'recent_inquiries': recent_inquiries,
    }
    
    return render(request, 'admin/dashboard.html', context)

def clear_cache():
    """Limpiar caché cuando se actualizan los datos"""
    cache.clear()
    imagekit_cache = get_cache()
    imagekit_cache.clear()