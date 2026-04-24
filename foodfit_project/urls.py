from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),
]

handler404 = custom_404
handler500 = custom_500
