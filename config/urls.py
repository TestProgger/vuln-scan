from django.contrib import admin
from django.urls import path, include
from project.processes.views import GetProcessTriggerMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('project.users.api.urls')),
    path('scenarios/', include('project.scenarios.api.urls')),
    path('process/get_message/', GetProcessTriggerMessageView.as_view({"post": "get_message"}))
]
