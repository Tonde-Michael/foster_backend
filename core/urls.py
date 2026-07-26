from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("GIS Parcel API is running")

urlpatterns = [
    path('', home),  # add this
    path('admin/', admin.site.urls),
    path('api/', include('gisapp.urls')),
]
