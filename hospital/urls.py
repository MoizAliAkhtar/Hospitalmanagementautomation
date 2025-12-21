from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('metrics/', include('django_prometheus.urls')),
    
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('doctors.urls')),
    path('', include('patients.urls')),
    path('', include('django_prometheus.urls')),
    

]
