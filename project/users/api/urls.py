from django.urls import path, include


urlpatterns = [
    path('auth/', include('project.users.api.auth.urls')),
    path('profile/', include('project.users.api.profile.urls') )
]