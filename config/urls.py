from django.contrib import admin
from django.urls import path, include
from project.processes.views import GetProcessTriggerMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('project.users.api.urls')),
    path('api/scenarios/', include('project.scenarios.api.urls')),
    path('api/processes/', include('project.processes.api.urls'))
]
