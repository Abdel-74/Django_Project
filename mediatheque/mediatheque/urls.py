from django.urls import path, include
from bibliothecaire import views as biblio_views

urlpatterns = [
    path('', biblio_views.accueil, name='accueil'),
    path('bibliothecaire/', include('bibliothecaire.urls')),
    path('membre/', include('membre.urls')),
]
