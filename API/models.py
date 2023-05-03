from django.db import models

# Create your models here.


class NanoIoT(models.Model):
    cmds = (
        ('screenshot', 'screenshot'),
        ('upgrade', 'upgrade'),
    )
    where = (
        ('emboutissage', 'emboutissage'),
        ('ferrage', 'ferrage'),
        ('montage', 'montage'),
        ('peinture', 'peinture'),
        ('o2x', 'o2x'),
        ('moteur', 'moteur'),
        ('unknown', 'unknown')
    )
    resolutions = (
        ('1366x673', '1366x673'), ('3840x2400', '3840x2400'), ('3840x2160', '3840x2160'), ('2880x1800', '2880x1800'),
        ('2560x1600', '2560x1600'), ('2560x1440', '2560x1440'), ('1920x1440', '1920x1440'), ('1856x1392', '1856x1392'),
        ('1792x1344', '1792x1344'), ('1920x1200', '1920x1200'), ('1920x1080', '1920x1080'), ('1600x1200', '1600x1200'),
        ('1680x1050', '1680x1050'), ('1400x1050', '1400x1050'), ('1280x1024', '1280x1024'), ('1440x900', '1440x900'),
        ('1280x960', '1280x960'), ('1360x768', '1360x768'), ('1280x800', '1280x800'), ('1152x864', '1152x864'),
        ('1280x768', '1280x768'), ('1280x720', '1280x720'), ('1024x768', '1024x768'), ('800x600', '800x600'),
        ('640x480', '640x480')
    )
    where_list = [where_tuple[0] for where_tuple in where]
    hostname = models.CharField(max_length=100, unique=True, default='dm')
    custom_cmd = models.TextField(blank=True, null=True)
    custom_cmd_output = models.TextField(blank=True, null=True)
    defined_cmds = models.CharField(max_length=20, choices=cmds, blank=True, null=True)
    what = models.TextField(max_length=100, default='cusm_cmd')
    where = models.CharField(max_length=20, choices=where, default='unknown')
    image = models.ImageField(upload_to='', null=True)
    dashboard_link = models.CharField(max_length=255, default='http://10.106.134.210:8080/d/lpU4hW3Mz/dashboard-montage2?orgId=1&refresh=1m&kiosk')
    resolution = models.CharField(max_length=20, choices=resolutions, default='1920x1080')

    def __str__(self):
        return self.hostname




