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
    where_list = [where_tuple[0] for where_tuple in where]
    hostname = models.CharField(max_length=100, unique=True, default='dm')
    custom_cmd = models.TextField(blank=True, null=True)
    custom_cmd_output = models.TextField(blank=True, null=True)
    defined_cmds = models.CharField(max_length=20, choices=cmds, blank=True, null=True)
    what = models.TextField(max_length=100, default='cusm_cmd')
    where = models.CharField(max_length=20, choices=where, default='unknown')
    image = models.ImageField(upload_to='', null=True)
    dashboard_link = models.CharField(max_length=255, default='http://10.106.134.210:8080/d/lpU4hW3Mz/dashboard-montage2?orgId=1&refresh=1m&kiosk')

    def __str__(self):
        return self.hostname




