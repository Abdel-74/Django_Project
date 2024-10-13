from django.urls import path
from . import views

app_name = 'membre'

urlpatterns = [
    path('medias-disponibles/', views.liste_medias_membre, name='liste_medias_membre'),
]
