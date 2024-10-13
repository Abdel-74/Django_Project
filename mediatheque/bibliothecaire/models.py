from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone


class Media(models.Model):
    TYPE_MEDIA = [
        ('livre', 'Livre'),
        ('cd', 'CD'),
        ('dvd', 'DVD'),
        ('jeu', 'Jeu de plateau'),
    ]

    titre = models.CharField(max_length=255)
    auteur_realisateur = models.CharField(max_length=255)
    type_media = models.CharField(choices=TYPE_MEDIA, max_length=10)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class Membre(models.Model):
    membre_id = models.CharField(max_length=20, unique=True, blank=True)  # Laisser vide pour l'auto-génération
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.membre_id:  # Si membre_id n'est pas défini
            total_membres = Membre.objects.count() + 1  # Calcule le total de membres
            self.membre_id = f'M{total_membres:04d}'  # Génère un ID du style "M0001"...
        super(Membre, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(blank=True, null=True)

    def clean(self):
        super().clean()

        # 1. Vérifier que le membre n'a pas déjà 3 emprunts actifs
        emprunts_actifs = Emprunt.objects.filter(membre=self.membre, date_retour__isnull=True).count()
        if emprunts_actifs >= 3:
            raise ValidationError(f"{self.membre.nom} {self.membre.prenom} a déjà 3 emprunts en cours.")

        # 2. Vérifier que le membre n'a pas d'emprunts en retard
        emprunts_en_retard = Emprunt.objects.filter(
            membre=self.membre,
            date_retour__isnull=True,
            date_emprunt__lt=timezone.now() - timedelta(days=7)
        ).exists()

        if emprunts_en_retard:
            raise ValidationError(f"{self.membre.nom} {self.membre.prenom} a des emprunts en retard et ne peut pas emprunter.")

        # 3. Empêcher l'emprunt de jeux de plateau
        if self.media.type_media == 'jeu':
            raise ValidationError("Les jeux de plateau ne peuvent pas être empruntés, uniquement consultés sur place.")

    def save(self, *args, **kwargs):
        # Gérer la disponibilité du média lors de la création ou du retour de l'emprunt
        if not self.pk:  # Nouvel emprunt
            self.media.disponible = False
            self.media.save()
        elif self.date_retour:  # Emprunt retourné
            self.media.disponible = True
            self.media.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Emprunt de {self.media} par {self.membre}"
