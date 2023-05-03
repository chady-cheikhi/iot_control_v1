import os
from django.views import View
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import NanoIoT

# Create your views here.


class IndexData(View):
    def get(self, request):
        nanos = NanoIoT.objects.all()
        data = {}
        for nano in nanos:
            data[nano.hostname] = {
                'hostname': nano.hostname
            }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class NanoTerminalData(View):

    def get(self, request, hostname):
        nanos_query = NanoIoT.objects.all().get(hostname=hostname)
        data = {
            'hostname': nanos_query.hostname,
            'id': nanos_query.pk,
            'custom_cmd': None if nanos_query.custom_cmd == "" else nanos_query.custom_cmd,
            'custom_cmd_output': nanos_query.custom_cmd_output,
            'where': nanos_query.where,
        }
        return JsonResponse(data)

    def post(self, request, hostname):
        nano = NanoIoT.objects.get(hostname=NanoIoT.objects.get(hostname=hostname))
        nano.custom_cmd = request.POST['custom_cmd']
        nano.custom_cmd_output = request.POST['custom_cmd_output']
        nano.save()
        return JsonResponse({
            'status': "commande envoyée"
        })


@method_decorator(csrf_exempt, name='dispatch')
class DefinedFct(View):

    def get(self, request, hostname):
        nano = NanoIoT.objects.all().get(hostname=hostname)

        return JsonResponse({'what': nano.what})

    def post(self, request, hostname):
        nano = NanoIoT.objects.all().get(hostname=hostname)
        if nano.what == 'screenshot':
            nano.image.delete(save=True)
            try:
                screenshot = request.FILES['screenshot']
                screenshot_name = 'screenshot_'+request.POST['image_name']+'.png'
                print(screenshot_name)
                nano.image.save(screenshot_name, screenshot)
                nano.what = ''
            except:
                nano.what = request.POST['what']
        else:
            nano.what = request.POST['what']
        nano.save()
        return JsonResponse({})


@method_decorator(csrf_exempt, name='dispatch')
class ShowDashboard(View):
    def get(self, request, hostname):
        nano = NanoIoT.objects.all().get(hostname=hostname)
        return JsonResponse({'what': nano.what,
                             'dashboard_link': nano.dashboard_link})

    def post(self, request, hostname):
        nano = NanoIoT.objects.all().get(hostname=hostname)
        nano.dashboard_link = request.POST['dashboard_link']
        print(nano.dashboard_link)
        nano.what = request.POST['what']
        nano.save()
        return JsonResponse({})


@method_decorator(csrf_exempt, name='dispatch')
class ChangeResolution(View):
    def get(self, request, hostname):
        nano = NanoIoT.objects.all().get(hostname=hostname)
        return JsonResponse({'what': nano.what,
                             'resolution': nano.resolution})

    def post(self, request, hostname):
        nano = NanoIoT.objects.all().get(hostname=hostname)
        nano.resolution = request.POST['resolution']
        print(nano.resolution)
        nano.what = request.POST['what']
        nano.save()
        return JsonResponse({})


