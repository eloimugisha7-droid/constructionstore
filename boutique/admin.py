from django.contrib import admin
from .models import Produit, Commande


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'stock', 'disponible')
    list_filter = ('categorie', 'disponible')
    search_fields = ('nom',)


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        'nom_client',
        'telephone',
        'produit',
        'quantite',
        'prix_unitaire',
        'total_commande',
        'statut',
        'date_commande',
        'cree_par_employe',
        'employe',
    )

    list_filter = ('statut', 'date_commande', 'cree_par_employe')
    search_fields = ('nom_client', 'telephone')
