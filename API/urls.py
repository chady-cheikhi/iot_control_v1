from django.urls import path
from .views import NanoTerminalData, IndexData, DefinedFct, Functionality


urlpatterns = [
    path('nano/', IndexData.as_view(), name='index-data'),
    path('nano/<str:hostname>/terminal', NanoTerminalData.as_view(), name='nano'),
    path('nano/<str:hostname>', DefinedFct.as_view(), name='defined-fct'),
    path('nano/<str:hostname>/<str:functionality>', Functionality.as_view(), name='functionality')
]
