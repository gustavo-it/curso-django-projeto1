from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('recipes.urls')),
    path('recipes/', include('recipes.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# O primeiro parâmetro é a variável MEDIA_URL, e o segundo é o seu valor
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
