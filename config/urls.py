from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path("schedule/", include("schedule.urls")),
    path("accounts/", include("accounts.urls")),
]
