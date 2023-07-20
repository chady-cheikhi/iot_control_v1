from django.urls import path
from .views import NanoTerminalData, IndexData, Screenshot, ShowDashboard, ChangeResolution, Upgrade, ShowVideo, FeedBack


urlpatterns = [
    path('nano/', IndexData.as_view(), name='index-data'),
    path('nano/<str:hostname>/terminal', NanoTerminalData.as_view(), name='nano'),
    path('nano/<str:hostname>', Screenshot.as_view(), name='screenshot'),
    path('nano/<str:hostname>/show_dashboard', ShowDashboard.as_view(), name='show_dashboard'),
    path('nano/<str:hostname>/change_resolution', ChangeResolution.as_view(), name='change_resolution'),
    path('nano/<str:hostname>/upgrade', Upgrade.as_view(), name='upgrade'),
    path('nano/<str:hostname>/show_video', ShowVideo.as_view(), name='show_video'),
    path('nano/<str:hostname>/feedback', FeedBack.as_view(), name='feedback'),
]
