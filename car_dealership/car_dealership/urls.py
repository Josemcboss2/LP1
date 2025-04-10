from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from autos.views import admin_dashboard

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),  # Add this before admin/ pattern
    path('admin/', admin.site.urls),
    path('', include('autos.urls')),  # Incluye las URLs de tu aplicación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL para cerrar sesión
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)