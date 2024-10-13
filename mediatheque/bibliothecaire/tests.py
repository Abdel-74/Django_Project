from django.test import TestCase
from django.utils import timezone
from bibliothecaire.models import Membre, Media, Emprunt
from django.core.exceptions import ValidationError


class EmpruntTestCase(TestCase):

    def setUp(self):
        # Création des objets de test
        self.membre = Membre.objects.create(nom="Dupont", prenom="Jean")
        self.media = Media.objects.create(titre="Les Misérables", auteur_realisateur="Victor Hugo", type_media="livre",
                                          disponible=True)

    def test_creer_emprunt(self):
        # Créer un emprunt
        emprunt = Emprunt.objects.create(membre=self.membre, media=self.media)

        # Vérifie si l'emprunt a été créé
        self.assertEqual(Emprunt.objects.count(), 1)
        self.assertEqual(emprunt.media, self.media)

        # Vérifie que le média est maintenant indisponible
        self.media.refresh_from_db()
        self.assertFalse(self.media.disponible)


class RetourEmpruntTestCase(TestCase):

    def setUp(self):
        # Création des objets de test
        self.membre = Membre.objects.create(nom="Durand", prenom="Claire")
        self.media = Media.objects.create(titre="1984", auteur_realisateur="George Orwell", type_media="livre",
                                          disponible=True)

        # Créer un emprunt
        self.emprunt = Emprunt.objects.create(membre=self.membre, media=self.media)

    def test_retourner_emprunt(self):
        # Retourner l'emprunt
        self.emprunt.date_retour = timezone.now()
        self.emprunt.media.disponible = True
        self.emprunt.save()

        # Vérifier si le média est à nouveau disponible
        self.media.refresh_from_db()
        self.assertTrue(self.media.disponible)

        # Vérifier que la date de retour est bien enregistrée
        self.assertIsNotNone(self.emprunt.date_retour)


class ContrainteEmpruntTestCase(TestCase):

    def setUp(self):
        # Création des objets de test
        self.membre = Membre.objects.create(nom="Martin", prenom="Paul")
        self.media1 = Media.objects.create(titre="Livre 1", auteur_realisateur="Auteur 1", type_media="livre",
                                           disponible=True)
        self.media2 = Media.objects.create(titre="Livre 2", auteur_realisateur="Auteur 2", type_media="livre",
                                           disponible=True)
        self.media3 = Media.objects.create(titre="Livre 3", auteur_realisateur="Auteur 3", type_media="livre",
                                           disponible=True)
        self.media4 = Media.objects.create(titre="Livre 4", auteur_realisateur="Auteur 4", type_media="livre",
                                           disponible=True)

    def test_limite_trois_emprunts(self):
        # Créer trois emprunts
        Emprunt.objects.create(membre=self.membre, media=self.media1)
        Emprunt.objects.create(membre=self.membre, media=self.media2)
        Emprunt.objects.create(membre=self.membre, media=self.media3)

        # Essayer de créer un quatrième emprunt pour le même membre
        emprunt4 = Emprunt(membre=self.membre, media=self.media4)
        with self.assertRaises(ValidationError):
            emprunt4.clean()
