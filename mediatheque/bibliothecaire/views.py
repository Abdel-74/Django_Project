from django.shortcuts import render, redirect, get_object_or_404
from .forms import MediaForm, MembreForm, EmpruntForm
from .models import Media, Membre, Emprunt
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone


def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/membre_list.html', {'membres': membres})

def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/media_list.html', {'medias': medias})

def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bibliothecaire:liste_medias')
    else:
        form = MediaForm()
    return render(request, 'bibliothecaire/ajouter_media.html', {'form': form})

def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bibliothecaire:liste_membres')
    else:
        form = MembreForm()
    return render(request, 'bibliothecaire/ajouter_membre.html', {'form': form})

def modifier_membre(request, membre_id):
    membre = get_object_or_404(Membre, membre_id=membre_id)

    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('bibliothecaire:liste_membres')  # Redirige vers la liste après la mise à jour
    else:
        form = MembreForm(instance=membre)

    return render(request, 'bibliothecaire/modifier_membre.html', {'form': form, 'membre': membre})

def liste_emprunt(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'bibliothecaire/emprunt_list.html', {'emprunts': emprunts})


def creer_emprunt(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)  # Ne pas sauvegarder immédiatement
            try:
                emprunt.clean()  # Effectue les vérifications (limite de 3 emprunts, retards...)
                emprunt.save()  # Sauvegarde si tout est correct
                emprunt.media.disponible = False  # Mettre à jour la disponibilité du média
                emprunt.media.save()
                messages.success(request, 'Emprunt créé avec succès.')
                return redirect('bibliothecaire:liste_emprunt')  # Redirige vers la liste des emprunts
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = EmpruntForm()

    return render(request, 'bibliothecaire/creer_emprunt.html', {'form': form})


def retourner_emprunt(request, membre_id, media_id):
    # Récupérer l'emprunt basé sur les IDs du membre et du média
    emprunt = get_object_or_404(Emprunt, membre_id=membre_id, media_id=media_id, date_retour__isnull=True)

    # Vérifie si l'emprunt n'a pas déjà été retourné
    if emprunt.date_retour is None:
        emprunt.date_retour = timezone.now()  # Marquer la date de retour actuelle
        emprunt.media.disponible = True  # Rendre le média disponible
        emprunt.media.save()
        emprunt.save()
        messages.success(request, f"Le média '{emprunt.media.titre}' a été rendu avec succès.")
    else:
        messages.warning(request, f"Le média '{emprunt.media.titre}' a déjà été retourné.")

    return redirect('bibliothecaire:liste_emprunt')


def accueil(request):
    return render(request, 'bibliothecaire/accueil.html')