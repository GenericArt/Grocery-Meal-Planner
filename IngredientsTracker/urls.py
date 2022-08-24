from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkscannedbarcode', views.check_scanned_barcode, name='check_scanned_barcode'),
    path('barcodescanned', views.barcode_scanned, name='barcode_scanned'),
    path("__reload__/", include("django_browser_reload.urls")),
]