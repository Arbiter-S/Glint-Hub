from .views import index
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Documents
    path("api/docs/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("products/", include("products.urls")),
    path("cart/", include("carts.urls")),
    path("orders/", include("orders.urls")),
    path("transactions/", include("transactions.urls")),
    path("", index, name="index"),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += debug_toolbar_urls()
