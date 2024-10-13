from django.urls import path
from . import views

app_name = 'bibliothecaire'

urlpatterns = [
    path('membres/', views.liste_membres, name='liste_membres'),
    path('ajouter-membre/', views.ajouter_membre, name='ajouter_membre'),
    path('medias/', views.liste_medias, name='liste_medias'),
    path('ajouter-media/', views.ajouter_media, name='ajouter_media'),
    path('modifier-membre/<str:membre_id>/', views.modifier_membre, name='modifier_membre'),
    path('emprunts/', views.liste_emprunt, name='liste_emprunt'),
    path('emprunts/creer/', views.creer_emprunt, name='creer_emprunt'),
    path('emprunts/retourner/<int:membre_id>/<int:media_id>/', views.retourner_emprunt, name='retourner_emprunt'),
]
