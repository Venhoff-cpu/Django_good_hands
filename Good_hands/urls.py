from django.contrib import admin
from django.urls import include, path

# Change default Dajngo Administration texts
admin.site.site_header = "Oddam w dobre ręce - Admin"
admin.site.site_title = "Portal administracji"
admin.site.index_title = "Witaj na portalu administracyjnym"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("charity.urls")),
]
