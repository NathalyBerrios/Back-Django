from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core import views
from core.api_views import RegistroViewSet

# El router genera solo las rutas de /api/registros/ y /api/registros/<id>/
router = DefaultRouter()
router.register(r"registros", RegistroViewSet, basename="registro")

urlpatterns = [
    path("admin/", admin.site.urls),

    # ---------- API (ES3) ----------
    # Token JWT: se pide con usuario y contraseña, y se refresca sin
    # volver a mandar la contraseña.
    path("api/token/", TokenObtainPairView.as_view(), name="api_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="api_token_refresh"),
    # Documentación (Swagger). Solo la ve quien inició sesión en /login/.
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/", include(router.urls)),

    # ---------- Pantallas HTML (ES2), sin cambios ----------
    path("", views.lista, name="lista"),
    path("registros/crear/", views.crear, name="crear"),
    path("registros/<int:pk>/editar/", views.editar, name="editar"),
    path("registros/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
    path("login/", views.vista_login, name="login"),
    path("logout/", views.vista_logout, name="logout"),
]
