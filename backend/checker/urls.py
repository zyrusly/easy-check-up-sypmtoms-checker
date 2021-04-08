from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.get_symptoms, name='symptoms'),
    path('diagnosis/', views.get_diagnosis, name='diagnosis'),
    # path('details/<int:issue_id>/',views.diag_details, name='details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)