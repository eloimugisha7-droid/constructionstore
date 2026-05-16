from django.db import models
from django.contrib.auth.models import User


class Produit(models.Model):
    CATEGORIES = [
        ('ciment', 'Ciment'),
        ('fer', 'Fer à béton'),
        ('brique', 'Briques'),
        ('tole', 'Tôles'),
        ('sable', 'Sable'),
        ('gravier', 'Gravier'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    description = models.TextField(blank=True)
    prix = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)

    def __str__(self):
        return self.nom


class Commande(models.Model):
    STATUTS = [
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    ]

    nom_client = models.CharField(max_length=200)
    telephone = models.CharField(max_length=30)
    adresse = models.CharField(max_length=255, blank=True)

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    prix_unitaire = models.FloatField(default=0)
    total_commande = models.FloatField(default=0)

    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='validee')

    cree_par_employe = models.BooleanField(default=False)
    employe = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def total(self):
        return self.total_commande

    def __str__(self):
        return f"{self.nom_client} - {self.produit.nom}"
