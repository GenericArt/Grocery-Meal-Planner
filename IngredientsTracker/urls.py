from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('checkscannedbarcode', views.check_scanned_barcode, name='check_scanned_barcode'),
    path('barcodescanned', views.barcode_scanned, name='barcode_scanned'),
    path('addnewitem', views.add_new_ingredient, name='add_new_item'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
