from django.contrib import admin
from .models import Quote_ovr,Quote_det
from import_export.admin import ImportExportModelAdmin

admin.site.register(Quote_ovr)
admin.site.register(Quote_det)
# Register your models here.
