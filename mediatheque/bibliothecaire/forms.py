from django import forms
from .models import Media, Membre, Emprunt


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'auteur_realisateur', 'type_media', 'disponible']


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'bloque']

class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['membre', 'media']

    def __init__(self, *args, **kwargs):
        super(EmpruntForm, self).__init__(*args, **kwargs)
        # Filtre les médias disponibles seulement
        self.fields['media'].queryset = Media.objects.filter(disponible=True)