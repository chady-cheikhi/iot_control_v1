from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import AddNewNanoForm
from django.views import View


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
        nano = NanoIoT.objects.all().get(hostname=hostname)
        functionalities = ['custom_cmd', 'reboot', 'screenshot', 'show_dashboard', 'show_video', 'change_resolution', 'upgrade']
        resolutions = [res[0] for res in list(NanoIoT.resolutions)]
        where_dict = {}
        for place in NanoIoT.where_list:
            where_dict[place] = list(NanoIoT.objects.filter(where=place).values_list('hostname', flat=True))
        nano.what = ''
        nano.custom_cmd = None
        nano.save()
        return render(request, 'nano_page.html', {'functionalities': functionalities,
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


@method_decorator(csrf_exempt, name='dispatch')
class AddNewNano(View):
    def get(self, request):
        new_nano_form = AddNewNanoForm()
        return render(request, 'add-new.html', {'form': new_nano_form})

    def post(self, request):
        hostname = request.POST['hostname']
        where = request.POST['where']
        new_nano = NanoIoT(hostname=hostname, where= where)
        new_nano.save()
        new_nano_form = AddNewNanoForm()
        return render(request, 'add-new.html', {'form': new_nano_form})




