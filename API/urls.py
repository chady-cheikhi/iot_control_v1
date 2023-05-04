from django.urls import path
from .views import NanoTerminalData, IndexData, DefinedFct, ShowDashboard, ChangeResolution, Upgrade, ShowVideo


urlpatterns = [
    path('nano/', IndexData.as_view(), name='index-data'),
    path('nano/<str:hostname>/terminal', NanoTerminalData.as_view(), name='nano'),
    path('nano/<str:hostname>', DefinedFct.as_view(), name='defined-fct'),
    path('nano/<str:hostname>/show_dashboard', ShowDashboard.as_view(), name='show_dashboard'),
    path('nano/<str:hostname>/change_resolution', ChangeResolution.as_view(), name='change_resolution'),
    path('nano/<str:hostname>/upgrade', Upgrade.as_view(), name='change_resolution'),
    path('nano/<str:hostname>/show_video', ShowVideo.as_view(), name='show_video'),
]
