# Generated by Django 5.1.1 on 2024-10-07 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('auteur_realisateur', models.CharField(max_length=255)),
                ('type_media', models.CharField(choices=[('livre', 'Livre'), ('cd', 'CD'), ('dvd', 'DVD'), ('jeu', 'Jeu de plateau')], max_length=10)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membre_id', models.CharField(blank=True, max_length=20, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bloque', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateTimeField(auto_now_add=True)),
                ('date_retour', models.DateTimeField(blank=True, null=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliothecaire.media')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliothecaire.membre')),
            ],
        ),
    ]
