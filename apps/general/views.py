from . import utils
from django.contrib import messages
from django.http import JsonResponse
from notifications.signals import notify
from notifications.models import Notification
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect


@login_required(login_url="users:login", redirect_field_name='next')
def search(request):
    return render(request, 'global/search.html')



################################################################################


@login_required(login_url="users:login", redirect_field_name='next')
def get_notifications(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "Erro. User não autenticado", "data": []})
    if request.method == 'GET':
        notifications = serialize('json', Notification.objects.all())
        print(notifications)
    return JsonResponse({"status": "sucegss", "data": notifications})

########################################################################################


@login_required(login_url="users:login", redirect_field_name='next')
def read_all_notifications(request):
    return render(request, "notifications/read-all-notifications.html", {})

###############################################################################################


@login_required(login_url="users:login", redirect_field_name='next')
def read_notification(request, id):
    notification = get_object_or_404(Notification, pk=id)
    notification.unread = False
    notification.save()
    return HttpResponseRedirect(notification.target.get_absolute_url())
    # return redirect(reverse('view-material-requisition', args=(notification.target.id,)))


#################################################################################
# @login_required(login_url="users:login", redirect_field_name='next')
# def send_notification_material_req(request, id):
#     requisition = get_object_or_404(RequisitionMaterial, pk=id)

#     if request.method == "POST":
#         email = request.POST.get("email")
#         description = request.POST.get("observation")
#         if email == "":
#             messages.error(request, "Campo de email vazio!")
#         elif User.objects.filter(email=email).exists():
#             mail_to = get_object_or_404(User, email=email)
#             notify.send(request.user, recipient=mail_to, verb="Pedido de Verificação de Requisição de Materias", target=requisition, description=description)
#             messages.success(request, f"Notificação enviada a {mail_to.get_full_name()}!")
#         else:
#             messages.error(request, "Este email não existe no sistema!")
#     return render(request, "notifications/send-notification-material-req.html", {"requisition":requisition})


@login_required(login_url="users:login", redirect_field_name='next')
def home(request):
    page = utils.get_sub_nav_headers("Dashboard", "Home", "Minha Dashboard")
    return render(request, "general/home.html", {"page": page})
