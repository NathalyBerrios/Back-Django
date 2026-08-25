from django.contrib import admin
from django.urls import path
from core.views import resumen

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', resumen, name='resumen'), # Esta línea conecta tu vista a la página principal
]