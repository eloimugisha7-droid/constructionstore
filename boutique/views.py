import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Produit, Commande


def accueil(request):
    produits = Produit.objects.filter(disponible=True)
    return render(request, 'boutique/accueil.html', {'produits': produits})


def commander(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        quantite = int(request.POST.get('quantite'))

        if quantite > produit.stock:
            messages.error(request, "Stock insuffisant.")
            return redirect('commander', produit_id=produit.id)

        total = produit.prix * quantite

        commande = Commande.objects.create(
            nom_client=request.POST.get('nom_client'),
            telephone=request.POST.get('telephone'),
            adresse=request.POST.get('adresse'),
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix,
            total_commande=total,
            cree_par_employe=False,
            statut='validee'
        )

        produit.stock -= quantite
        produit.save()

        return redirect('ticket', commande_id=commande.id)

    return render(request, 'boutique/commander.html', {'produit': produit})


@login_required
def dashboard_employe(request):
    aujourd_hui = timezone.now().date()

    commandes_jour = Commande.objects.filter(
        date_commande__date=aujourd_hui,
        statut='validee'
    )

    chiffre_affaires = commandes_jour.aggregate(
        total=Sum('total_commande')
    )['total'] or 0

    nombre_commandes = commandes_jour.count()

    nombre_clients = commandes_jour.values('telephone').distinct().count()

    produits_vendus = commandes_jour.aggregate(
        total=Sum('quantite')
    )['total'] or 0

    stock = Produit.objects.all()

    commandes_recentes = Commande.objects.order_by('-date_commande')[:10]

    return render(request, 'boutique/dashboard_employe.html', {
        'chiffre_affaires': chiffre_affaires,
        'nombre_commandes': nombre_commandes,
        'nombre_clients': nombre_clients,
        'produits_vendus': produits_vendus,
        'stock': stock,
        'commandes_recentes': commandes_recentes,
    })


@login_required
def nouvelle_commande(request):
    produits = Produit.objects.filter(disponible=True)

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        produit = get_object_or_404(Produit, id=produit_id)

        quantite = int(request.POST.get('quantite'))

        if quantite > produit.stock:
            messages.error(request, "Stock insuffisant pour ce produit.")
            return redirect('nouvelle_commande')

        total = produit.prix * quantite

        commande = Commande.objects.create(
            nom_client=request.POST.get('nom_client'),
            telephone=request.POST.get('telephone'),
            adresse=request.POST.get('adresse'),
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix,
            total_commande=total,
            cree_par_employe=True,
            employe=request.user,
            statut='validee'
        )

        produit.stock -= quantite
        produit.save()

        return redirect('ticket', commande_id=commande.id)

    return render(request, 'boutique/nouvelle_commande.html', {
        'produits': produits
    })


@login_required
def liste_commandes(request):
    commandes = Commande.objects.order_by('-date_commande')
    return render(request, 'boutique/liste_commandes.html', {
        'commandes': commandes
    })


@login_required
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    if commande.statut == 'validee':
        commande.produit.stock += commande.quantite
        commande.produit.save()

        commande.statut = 'annulee'
        commande.save()

        messages.success(request, "Commande annulée. Le stock a été remis à jour.")
    else:
        messages.error(request, "Cette commande est déjà annulée.")

    return redirect('liste_commandes')


def ticket(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'boutique/ticket.html', {
        'commande': commande
    })
@login_required
def exporter_ventes(request):
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    commandes = Commande.objects.filter(statut='validee')

    if date_debut:
        commandes = commandes.filter(date_commande__date__gte=date_debut)

    if date_fin:
        commandes = commandes.filter(date_commande__date__lte=date_fin)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventes.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Date',
        'Client',
        'Telephone',
        'Produit',
        'Quantite',
        'Prix unitaire',
        'Total',
        'Employe'
    ])

    for commande in commandes:
        writer.writerow([
            commande.date_commande.strftime('%d/%m/%Y %H:%M'),
            commande.nom_client,
            commande.telephone,
            commande.produit.nom,
            commande.quantite,
            commande.prix_unitaire,
            commande.total_commande,
            commande.employe.username if commande.employe else 'Client en ligne'
        ])

    return response