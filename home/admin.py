from django.contrib import admin
from import_export import resources
from .models import User,Task
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        fields = ('title','supplier_name','cell_phone','contract_no','types_of_security','form_of_Security','issuing_bank',
    'Reference_no','issuing_date','expiry_date','amount')

class TaskAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TaskResource
    list_display = ['title','supplier_name','cell_phone','contract_no','types_of_security','form_of_Security','issuing_bank',
    'Reference_no','issuing_date','expiry_date','amount']

admin.site.register(User)
admin.site.register(Task,TaskAdmin)