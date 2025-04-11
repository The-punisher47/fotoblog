#<!-- filepath: d:\Desktop\fotoblog\fotoblog\blog\templates\blog\views.py -->

from django.shortcuts import render
from .models import Jante, Notification  # Assurez-vous que le modèle Jante et Notification existent

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import JanteForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import xlsxwriter
from io import BytesIO


@login_required
def home(request):
    # Récupérer les dernières notifications ou actions
    recent_activities = Notification.objects.all().order_by('-created_at')[:5]  # Les 5 dernières notifications

    return render(request, 'blog/home.html', {
        'user': request.user,
        'recent_activities': recent_activities,
    })

@login_required
def tableau_view(request):
    jantes = Jante.objects.all()  # Récupère toutes les jantes
    return render(request, 'blog/tableau.html', {'jantes': jantes})


@login_required
def NOTIFICATIONS_view(request):
    notifications = Notification.objects.all().order_by('-created_at')  # Trier par date décroissante
    return render(request, 'blog/NOTIFICATIONS.html', {'notifications': notifications})

@login_required
def tableau_bord_view(request):
    has_unread_notifications = Notification.objects.filter(is_read=False).exists()
    jantes = Jante.objects.all()
    total_jantes = jantes.count()
    jantes_en_service = jantes.exclude(prochain_ndi="HS").count()
    jantes_hors_service = jantes.filter(prochain_ndi="HS").count()
    return render(request, 'blog/TABLEAU_BORD.html', {
        'total_jantes': total_jantes,
        'jantes_en_service': jantes_en_service,
        'jantes_hors_service': jantes_hors_service,
        'has_unread_notifications': has_unread_notifications,
    })

@login_required
def gestion_view(request):
    has_unread_notifications = Notification.objects.filter(is_read=False).exists()
    jantes = Jante.objects.all()
    return render(request, 'blog/gestion.html', {
        'jantes': jantes,
        'has_unread_notifications': has_unread_notifications,
    })

@login_required
def add_jante_view(request):
    if request.method == 'POST':
        form = JanteForm(request.POST)
        if form.is_valid():
            jante = form.save(commit=False)
            # Définir les valeurs par défaut
            jante.nombre_de_deposes = 0
            jante.dernier_ndi = 0
            jante.prochain_ndi = 5  # Définit prochain_ndi à 5 par défaut
            jante.save()
            return redirect('gestion')  # Redirige vers la page GESTION après l'ajout
    else:
        form = JanteForm()
    return render(request, 'blog/add_jante.html', {'form': form})

#ajout pour add 



@csrf_exempt
def ajouter_depose(request, jante_id):
    if request.method == "POST":
        try:
            jante = Jante.objects.get(id=jante_id)
            jante.nombre_de_deposes += 1
            jante.update_ndi_values()  # Cette méthode doit mettre à jour les champs NDI
            jante.save()
            return JsonResponse({
                'success': True,
                'nombre_de_deposes': jante.nombre_de_deposes,
                'dernier_ndi': jante.dernier_ndi,  # Obligatoire
                'prochain_ndi': jante.prochain_ndi   # Obligatoire
            })
        except Jante.DoesNotExist:
            return JsonResponse({"success": False, "message": "Jante introuvable."})
    return JsonResponse({"success": False, "message": "Méthode non autorisée."})


@csrf_exempt
def retirer_depose(request, jante_id):
    if request.method == "POST":
        try:
            jante = Jante.objects.get(id=jante_id)
            if jante.nombre_de_deposes > 0:
                jante.nombre_de_deposes -= 1
                jante.update_ndi_values()  # Cette méthode doit mettre à jour les champs NDI
                jante.save()
                return JsonResponse({
                    'success': True,
                    'nombre_de_deposes': jante.nombre_de_deposes,
                    'dernier_ndi': jante.dernier_ndi,  # Obligatoire
                    'prochain_ndi': jante.prochain_ndi   # Obligatoire
                })
        except Jante.DoesNotExist:
            return JsonResponse({"success": False, "message": "Jante introuvable."})
    return JsonResponse({"success": False, "message": "Méthode non autorisée."})


@csrf_exempt
def update_obs(request, jante_id):
    if request.method == "POST":
        try:
            jante = Jante.objects.get(id=jante_id)
            obs_value = request.POST.get("obs", "")
            jante.obs = obs_value
            jante.save()
            return JsonResponse({"success": True, "obs": jante.obs})
        except Jante.DoesNotExist:
            return JsonResponse({"success": False, "message": "Jante introuvable."})
    return JsonResponse({"success": False, "message": "Méthode non autorisée."})


@login_required
def export_table_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tableau_gestion.pdf"'

    # Créer le PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, "Tableau de Gestion des Jantes")

    # Récupérer les données
    jantes = Jante.objects.all()
    y = 700
    for jante in jantes:
        pdf.drawString(50, y, f"Part Number: {jante.part_number}, Category: {jante.category}, Serial Number: {jante.serial_number}")
        y -= 20

    pdf.save()
    return response

@login_required
def export_table_excel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Ajouter les en-têtes
    headers = ['Part Number', 'Category', 'Serial Number', 'Support', 'Nombre de Déposes', 'Dernier NDI', 'Prochain NDI', 'OBS']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Ajouter les données
    jantes = Jante.objects.all()
    for row_num, jante in enumerate(jantes, start=1):
        worksheet.write(row_num, 0, jante.part_number)
        worksheet.write(row_num, 1, jante.category)
        worksheet.write(row_num, 2, jante.serial_number)
        worksheet.write(row_num, 3, jante.support)
        worksheet.write(row_num, 4, jante.nombre_de_deposes)
        worksheet.write(row_num, 5, jante.dernier_ndi)
        worksheet.write(row_num, 6, jante.prochain_ndi)
        worksheet.write(row_num, 7, jante.obs)

    workbook.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tableau_gestion.xlsx"'
    return response

@login_required
def mark_notifications_as_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)  # Marque toutes les notifications comme lues
    return JsonResponse({"success": True})

@login_required
def check_unread_notifications(request):
    has_unread_notifications = Notification.objects.filter(is_read=False).exists()
    return JsonResponse({"has_unread_notifications": has_unread_notifications})



