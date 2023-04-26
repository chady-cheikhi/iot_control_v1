from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from API.models import NanoIoT


# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'index.html')
class Nano(View):
    def get(self, request, hostname):
        functionalities = ['custom_cmd', 'reboot', 'screenshot', 'show_dashboard', 'show_video']
        nano = NanoIoT.objects.all().get(hostname=hostname)
        nano.what = ''
        nano.custom_cmd = None
        nano.save()
        return render(request, 'nano_reactive.html',
                      {'functionalities': functionalities,
                       'hostname': hostname})


class Terminal(View):
    def get(self, request, hostname):
        print('test')
        nano = NanoIoT.objects.all().get(hostname=hostname)
        nano.custom_cmd = None
        nano.custom_cmd_output = None
        nano.save()
        return render(request, "terminal.html", {
            'hostname': hostname
        })


class Screenshot(View):
    def get(self, request, hostname):
        return render(request, 'screenshot.html', {'hostname':hostname})



