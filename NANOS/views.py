from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from API.models import NanoIoT


# Create your views here.


class Index(View):
    def get(self, request):
        where_dict = {}
        for place in NanoIoT.where_list:
            where_dict[place] = list(NanoIoT.objects.filter(where=place).values_list('hostname', flat=True))
        print(where_dict)
        return render(request, 'index.html', {'where_dict': where_dict})


class Nano(View):
    def get(self, request, hostname):
        resolutions = ['2160x1278', '1366x673', '3840x2400', '3840x2160', '2880x1800', '2560x1600', '2560x1440', '1920x1440', '1856x1392', '1792x1344', '1920x1200', '1920x1080', '1600x1200', '1680x1050', '1400x1050', '1280x1024', '1440x900','1280x960', '1360x768', '1280x800', '1152x864', '1280x768', '1280x720', '1024x768', '800x600', '640x480']
        functionalities = ['custom_cmd', 'reboot', 'screenshot', 'show_dashboard', 'show_video', 'change_resolution', 'upgrade']
        nano = NanoIoT.objects.all().get(hostname=hostname)
        where_dict = {}
        for place in NanoIoT.where_list:
            where_dict[place] = list(NanoIoT.objects.filter(where=place).values_list('hostname', flat=True))
        nano.what = ''
        nano.custom_cmd = None
        nano.save()
        return render(request, 'nano_reactive.html', {'functionalities': functionalities,
                                                      'hostname': hostname,
                                                      'where_dict': where_dict,
                                                      'resolutions': resolutions
                                                      })


class Terminal(View):
    def get(self, request, hostname):
        where_dict = {}
        for place in NanoIoT.where_list:
            where_dict[place] = list(NanoIoT.objects.filter(where=place).values_list('hostname', flat=True))
        nano = NanoIoT.objects.all().get(hostname=hostname)
        nano.custom_cmd = None
        nano.custom_cmd_output = None
        nano.save()
        return render(request, "terminal.html", {
            'hostname': hostname,
            'where_dict': where_dict
        })


class Screenshot(View):
    def get(self, request, hostname):
        nano = NanoIoT.objects.get(hostname=hostname)
        image = nano.image
        print(image.name)
        return render(request, 'screenshot.html', {'hostname': hostname,
                                                   'image': image})


class Landing(View):
    def get(self, request):
        return render(request, 'landing.html')



