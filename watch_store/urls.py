from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('', include('home.urls')),
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('contact/', include('contact_request.urls')),
    path('policies/', include('policies.urls')),
    path('profile/', include('profiles.urls')),
    path('shop/', include('shop.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler404 = 'watch_store.views.handler404'
handler500 = 'watch_store.views.handler500'
