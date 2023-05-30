from django.contrib import admin
from .models import Location, User, Incident
from django.contrib.admin import AdminSite
# from django.contrib.admin import AdminSite
# from django.utils.translation import ugettext_lazy


# Register your models here.

admin.site.register(Location)
admin.site.register(Incident)
admin.site.register(User)

admin.site.site_header = 'Emergency Response Management System'
admin.site.index_title = 'ERMS Login Portal'
admin.site.site_title = 'Emergency Response Management System'

# Data Visualization
# class MyAdminSite(AdminSite):
#     site_url = 'http://127.0.0.1:8050/'

# admin_site = MyAdminSite(name='Visualize')
