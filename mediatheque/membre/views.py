from django.shortcuts import render
from bibliothecaire.models import Media


def liste_medias_membre(request):
    medias = Media.objects.all()
    return render(request, 'membre/media_list.html', {'medias': medias})
