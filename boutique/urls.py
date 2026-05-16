from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('commander/<int:produit_id>/', views.commander, name='commander'),

    path('employe/dashboard/', views.dashboard_employe, name='dashboard_employe'),
    path('employe/nouvelle-commande/', views.nouvelle_commande, name='nouvelle_commande'),
    path('employe/commandes/', views.liste_commandes, name='liste_commandes'),
    path('employe/annuler-commande/<int:commande_id>/', views.annuler_commande, name='annuler_commande'),
    path('employe/exporter-ventes/', views.exporter_ventes, name='exporter_ventes'),

    path('ticket/<int:commande_id>/', views.ticket, name='ticket'),
]